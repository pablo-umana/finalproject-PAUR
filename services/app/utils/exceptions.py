class AuthenticationError(Exception):
    """Excepción para errores de autenticación."""
    pass

class AuthorizationError(Exception):
    """Excepción para errores de autorización."""
    pass

class ValidationError(Exception):
    """Excepción para errores de validación."""
    pass

class ResourceError(Exception):
    """Excepción para errores relacionados con recursos."""
    pass