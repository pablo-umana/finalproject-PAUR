import { TemplateVariableGroup } from "@/types/template";

const mockVariableGroups: TemplateVariableGroup[] = [
    {
        id: "personal",
        name: "Datos Personales",
        variables: [
            {
                id: "nombre",
                name: "Nombre Completo",
                key: "{{nombre}}",
                type: "text",
                description: "Nombre completo del titular"
            },
            {
                id: "rut",
                name: "RUT",
                key: "{{rut}}",
                type: "text",
                description: "RUT del titular"
            },
            {
                id: "fecha_nacimiento",
                name: "Fecha de Nacimiento",
                key: "{{fecha_nacimiento}}",
                type: "date",
                description: "Fecha de nacimiento del titular"
            }
        ]
    },
    {
        id: "documento",
        name: "Datos del Documento",
        variables: [
            {
                id: "fecha_emision",
                name: "Fecha de Emisión",
                key: "{{fecha_emision}}",
                type: "date",
                description: "Fecha de emisión del documento"
            },
            {
                id: "numero_documento",
                name: "Número de Documento",
                key: "{{numero_documento}}",
                type: "text",
                description: "Número único del documento"
            },
            {
                id: "firma_digital",
                name: "Firma Digital",
                key: "{{firma_digital}}",
                type: "signature",
                description: "Firma digital del documento"
            }
        ]
    }
];

export const getVariableGroups = async (): Promise<TemplateVariableGroup[]> => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(mockVariableGroups);
        }, 500);
    });
};