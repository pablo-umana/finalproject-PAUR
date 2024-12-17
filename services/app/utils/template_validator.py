from typing import List, Dict, Optional
from app.utils.exceptions import ValidationError
from app.repositories.variable_repository import VariableRepository

class TemplateValidator:
    def __init__(self):
        self.variable_repository = VariableRepository()

    def validate_structure(self, content: dict) -> bool:
        """
        Valida la estructura básica (header, body, footer).

        Args:
            content: Diccionario con el contenido de la plantilla

        Returns:
            bool: True si la estructura es válida

        Raises:
            ValidationError: Si la estructura no es válida
        """
        required_sections = ['header', 'body', 'footer']

        # Verificar que existan todas las secciones requeridas
        for section in required_sections:
            if section not in content:
                raise ValidationError(f"Falta la sección '{section}' en la plantilla")

            if not content[section]:
                raise ValidationError(f"La sección '{section}' está vacía")

        # Verificar que no haya secciones adicionales
        extra_sections = set(content.keys()) - set(required_sections)
        if extra_sections:
            raise ValidationError(f"Secciones no permitidas: {', '.join(extra_sections)}")

        return True

    def validate_variables(self, content: dict, template_id: int) -> bool:
        """
        Valida que las variables usadas existan y sean válidas.

        Args:
            content: Diccionario con el contenido de la plantilla
            template_id: ID de la plantilla

        Returns:
            bool: True si todas las variables son válidas

        Raises:
            ValidationError: Si hay variables inválidas o no existentes
        """
        # Obtener todas las variables definidas para la plantilla
        template_variables = self.variable_repository.find_by_template_id(template_id)
        valid_variables = {var.name for var in template_variables}

        # Extraer variables usadas en el contenido
        used_variables = self._extract_variables(content)

        # Verificar que todas las variables usadas estén definidas
        undefined_variables = used_variables - valid_variables
        if undefined_variables:
            raise ValidationError(
                f"Variables no definidas: {', '.join(undefined_variables)}"
            )

        return True

    def validate_resources(self, content: dict, resources: List[dict]) -> bool:
        """
        Valida que los recursos referenciados existan y sean válidos.

        Args:
            content: Diccionario con el contenido de la plantilla
            resources: Lista de recursos disponibles

        Returns:
            bool: True si todos los recursos son válidos

        Raises:
            ValidationError: Si hay recursos inválidos o no existentes
        """
        # Extraer recursos referenciados en el contenido
        referenced_resources = self._extract_resources(content)
        available_resources = {res['resource_path'] for res in resources}

        # Verificar que todos los recursos referenciados estén disponibles
        missing_resources = referenced_resources - available_resources
        if missing_resources:
            raise ValidationError(
                f"Recursos no encontrados: {', '.join(missing_resources)}"
            )

        return True

    def _extract_variables(self, content: dict) -> set:
        """
        Extrae todas las variables usadas en el contenido.

        Args:
            content: Diccionario con el contenido de la plantilla

        Returns:
            set: Conjunto de nombres de variables encontradas
        """
        variables = set()

        def extract_from_text(text: str) -> None:
            """Extrae variables de un texto usando expresiones regulares."""
            import re
            # Buscar patrones como {{variable}} o {{ variable }}
            pattern = r'{{\s*([a-zA-Z][a-zA-Z0-9_]*)\s*}}'
            matches = re.finditer(pattern, text)
            for match in matches:
                variables.add(match.group(1))

        # Procesar cada sección
        for section in content.values():
            if isinstance(section, str):
                extract_from_text(section)
            elif isinstance(section, dict):
                for value in section.values():
                    if isinstance(value, str):
                        extract_from_text(value)

        return variables

    def _extract_resources(self, content: dict) -> set:
        """
        Extrae todas las referencias a recursos en el contenido.

        Args:
            content: Diccionario con el contenido de la plantilla

        Returns:
            set: Conjunto de rutas de recursos encontradas
        """
        resources = set()

        def extract_from_text(text: str) -> None:
            """Extrae referencias a recursos usando expresiones regulares."""
            import re
            # Buscar patrones como src="resources/..." o url('resources/...')
            patterns = [
                r'src=[\'"](resources/[^\'"]+)[\'"]',
                r'url\([\'"]?(resources/[^\'"]+)[\'"]?\)',
            ]
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    resources.add(match.group(1))

        # Procesar cada sección
        for section in content.values():
            if isinstance(section, str):
                extract_from_text(section)
            elif isinstance(section, dict):
                for value in section.values():
                    if isinstance(value, str):
                        extract_from_text(value)

        return resources

    def validate_all(self, content: dict, template_id: int, resources: List[dict]) -> bool:
        """
        Ejecuta todas las validaciones.

        Args:
            content: Diccionario con el contenido de la plantilla
            template_id: ID de la plantilla
            resources: Lista de recursos disponibles

        Returns:
            bool: True si todas las validaciones pasan

        Raises:
            ValidationError: Si alguna validación falla
        """
        self.validate_structure(content)
        self.validate_variables(content, template_id)
        self.validate_resources(content, resources)
        return True