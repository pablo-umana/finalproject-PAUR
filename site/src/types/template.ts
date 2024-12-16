export interface TemplateVariable {
    id: string;
    name: string;
    key: string;
    type: 'text' | 'date' | 'number' | 'currency' | 'signature';
    defaultValue?: string;
    description?: string;
}

export interface TemplateVariableGroup {
    id: string;
    name: string;
    variables: TemplateVariable[];
}

export interface Template {
    id: string;
    name: string;
    description?: string;
    content: {
        header: string;
        body: string;
        footer: string;
    };
    version: string;
    status: 'draft' | 'published';
    createdAt: string;
    updatedAt: string;
    createdBy: string;
}

export interface TemplateVersion {
    id: string;
    templateId: string;
    version: string;
    content: {
        header: string;
        body: string;
        footer: string;
    };
    changes: string;
    createdAt: string;
    createdBy: string;
}

export interface SaveTemplateRequest {
    name: string;
    description?: string;
    content: {
        header: string;
        body: string;
        footer: string;
    };
}