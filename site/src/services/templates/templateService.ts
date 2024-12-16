import { SaveTemplateRequest, Template, TemplateVersion } from "@/types/template";

// Simular guardado automático
let autoSaveTimeout: NodeJS.Timeout;

export const saveTemplate = async (template: SaveTemplateRequest): Promise<Template> => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                id: Math.random().toString(36).substr(2, 9),
                ...template,
                version: "1.0.0",
                status: "draft",
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                createdBy: "Usuario Actual" // En producción, obtener del contexto de autenticación
            });
        }, 1000);
    });
};

export const autoSaveTemplate = (template: SaveTemplateRequest, callback: (saved: Template) => void) => {
    if (autoSaveTimeout) {
        clearTimeout(autoSaveTimeout);
    }

    autoSaveTimeout = setTimeout(async () => {
        try {
            const saved = await saveTemplate(template);
            callback(saved);
        } catch (error) {
            console.error("Error en autoguardado:", error);
        }
    }, 2000); // Guardar después de 2 segundos de inactividad
};

export const publishTemplate = async (templateId: string): Promise<Template> => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                id: templateId,
                name: "Plantilla de ejemplo",
                content: {
                    header: "",
                    body: "",
                    footer: ""
                },
                version: "1.0.0",
                status: "published",
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                createdBy: "Usuario Actual"
            });
        }, 1000);
    });
};

export const getTemplateVersions = async (templateId: string): Promise<TemplateVersion[]> => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve([
                {
                    id: "v1",
                    templateId,
                    version: "1.0.0",
                    content: {
                        header: "",
                        body: "",
                        footer: ""
                    },
                    changes: "Versión inicial",
                    createdAt: new Date().toISOString(),
                    createdBy: "Usuario Actual"
                }
            ]);
        }, 500);
    });
};