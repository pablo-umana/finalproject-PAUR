export interface Document {
    id: string;
    name: string;
    type: string;
    status: "draft" | "pending" | "completed";
    createdAt: string;
    updatedAt: string;
    createdBy: string;
    content?: string;
    downloadUrl?: string;
    version?: string;
    description?: string;
    tags?: string[];
}

export interface DocumentFilter {
    search: string;
    status?: "draft" | "pending" | "completed";
    dateFrom?: string;
    dateTo?: string;
}

export interface DocumentVersion {
    id: string;
    documentId: string;
    versionNumber: string;
    createdAt: string;
    createdBy: string;
    changes: string;
    downloadUrl: string;
    status: "active" | "archived";
}

export interface DocumentDetail extends Document {
    content: string;
    version: string;
    description: string;
    tags: string[];
    downloadUrl: string;
    versions?: DocumentVersion[];
}
