import { Document, DocumentFilter, DocumentDetail, DocumentHistory, DocumentVersion } from "@/types/document";

const mockDocuments: Document[] = [
    {
        id: "1",
        name: "Contrato de Servicios",
        type: "Contrato",
        status: "completed",
        createdAt: "2024-02-20T10:00:00Z",
        updatedAt: "2024-02-20T11:30:00Z",
        createdBy: "Juan Pérez",
    },
    {
        id: "2",
        name: "Certificado de Residencia",
        type: "Certificado",
        status: "pending",
        createdAt: "2024-02-19T15:00:00Z",
        updatedAt: "2024-02-19T15:00:00Z",
        createdBy: "María González",
    },
    // Agrega más documentos mock aquí
];

const mockHistory: DocumentHistory[] = [
    {
        id: "1",
        documentId: "1",
        action: "created",
        description: "Documento creado",
        performedBy: "Juan Pérez",
        performedAt: "2024-02-20T10:00:00Z",
    },
    {
        id: "2",
        documentId: "1",
        action: "updated",
        description: "Actualización de contenido",
        performedBy: "María González",
        performedAt: "2024-02-20T11:30:00Z",
    },
    {
        id: "3",
        documentId: "1",
        action: "downloaded",
        description: "Documento descargado",
        performedBy: "Juan Pérez",
        performedAt: "2024-02-21T09:15:00Z",
    },
];

const mockVersions: DocumentVersion[] = [
    {
        id: "v3",
        documentId: "1",
        versionNumber: "1.2.0",
        createdAt: "2024-02-21T09:15:00Z",
        createdBy: "Juan Pérez",
        changes: "Actualización de cláusulas legales",
        downloadUrl: "/api/documents/1/versions/v3",
        status: "active",
    },
    {
        id: "v2",
        documentId: "1",
        versionNumber: "1.1.0",
        createdAt: "2024-02-20T11:30:00Z",
        createdBy: "María González",
        changes: "Corrección de términos y condiciones",
        downloadUrl: "/api/documents/1/versions/v2",
        status: "archived",
    },
    {
        id: "v1",
        documentId: "1",
        versionNumber: "1.0.0",
        createdAt: "2024-02-20T10:00:00Z",
        createdBy: "Juan Pérez",
        changes: "Versión inicial del documento",
        downloadUrl: "/api/documents/1/versions/v1",
        status: "archived",
    },
];

export const getDocuments = async (filters: DocumentFilter): Promise<Document[]> => {
    // Simulamos una llamada API con filtros
    return new Promise((resolve) => {
        setTimeout(() => {
            let filtered = [...mockDocuments];

            if (filters.search) {
                const searchLower = filters.search.toLowerCase();
                filtered = filtered.filter(
                    (doc) =>
                        doc.name.toLowerCase().includes(searchLower) ||
                        doc.type.toLowerCase().includes(searchLower) ||
                        doc.createdBy.toLowerCase().includes(searchLower)
                );
            }

            if (filters.status) {
                filtered = filtered.filter((doc) => doc.status === filters.status);
            }

            if (filters.dateFrom) {
                filtered = filtered.filter((doc) => doc.createdAt >= filters.dateFrom!);
            }

            if (filters.dateTo) {
                filtered = filtered.filter((doc) => doc.createdAt <= filters.dateTo!);
            }

            resolve(filtered);
        }, 500);
    });
};

export const getDocumentById = async (id: string): Promise<DocumentDetail> => {
    // Simulamos una llamada API
    return new Promise((resolve) => {
        setTimeout(() => {
            const document = mockDocuments.find((doc) => doc.id === id);
            if (document) {
                resolve({
                    ...document,
                    content: "Contenido detallado del documento...",
                    version: "1.0.0",
                    description: "Descripción completa del documento",
                    tags: ["importante", "legal", "2024"],
                    downloadUrl: `/api/documents/${id}/download`,
                });
            }
        }, 500);
    });
};

export const downloadDocument = async (id: string): Promise<Blob> => {
    // Simulamos una descarga de archivo
    return new Promise((resolve) => {
        setTimeout(() => {
            // Creamos un blob de ejemplo
            const content = "Contenido del documento PDF";
            const blob = new Blob([content], { type: "application/pdf" });
            resolve(blob);
        }, 1000);
    });
};

export const getDocumentHistory = async (documentId: string): Promise<DocumentHistory[]> => {
    return new Promise((resolve) => {
        setTimeout(() => {
            const history = mockHistory.filter((h) => h.documentId === documentId);
            resolve(history);
        }, 500);
    });
};

export const getDocumentVersions = async (documentId: string): Promise<DocumentVersion[]> => {
    return new Promise((resolve) => {
        setTimeout(() => {
            const versions = mockVersions.filter((v) => v.documentId === documentId);
            resolve(versions.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()));
        }, 500);
    });
};

export const downloadVersion = async (versionId: string): Promise<Blob> => {
    return new Promise((resolve) => {
        setTimeout(() => {
            const content = `Contenido de la versión ${versionId}`;
            const blob = new Blob([content], { type: "application/pdf" });
            resolve(blob);
        }, 1000);
    });
};
