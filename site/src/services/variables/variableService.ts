import axios from 'axios';
import { getToken } from '../auth/authService';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export interface Variable {
    variable_id: number;
    template_id: number;
    name: string;
    default_value?: string;
    required: boolean;
    variable_type: string;
    validation_rules?: ValidationRule[];
    created_at?: string;
    updated_at?: string;
}

export interface ValidationRule {
    type: string;
    params: Record<string, any>;
    message: string;
}

export interface CreateVariableRequest {
    template_id: number;
    name: string;
    default_value?: string;
    required?: boolean;
    variable_type: string;
    validation_rules?: ValidationRule[];
}

export interface UpdateVariableRequest {
    default_value?: string;
    required?: boolean;
    validation_rules?: ValidationRule[];
}

const getAuthHeaders = () => ({
    headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json'
    }
});

export const variableService = {
    async getVariables(templateId?: number) {
        const params = templateId ? { template_id: templateId } : {};
        const response = await axios.get(`${API_URL}/variables`, {
            ...getAuthHeaders(),
            params
        });
        return response.data.data;
    },

    async getVariable(variableId: number): Promise<Variable> {
        const response = await axios.get(`${API_URL}/variables/${variableId}`, getAuthHeaders());
        return response.data.data;
    },

    async createVariable(data: CreateVariableRequest): Promise<Variable> {
        const response = await axios.post(`${API_URL}/variables`, data, getAuthHeaders());
        return response.data.data;
    },

    async updateVariable(variableId: number, data: UpdateVariableRequest): Promise<Variable> {
        const response = await axios.put(`${API_URL}/variables/${variableId}`, data, getAuthHeaders());
        return response.data.data;
    },

    async deleteVariable(variableId: number): Promise<void> {
        await axios.delete(`${API_URL}/variables/${variableId}`, getAuthHeaders());
    },

    async bulkCreateVariables(templateId: number, variables: CreateVariableRequest[]): Promise<Variable[]> {
        const response = await axios.post(
            `${API_URL}/templates/${templateId}/variables/bulk`,
            { variables },
            getAuthHeaders()
        );
        return response.data.data;
    },

    async getPredefinedVariables(): Promise<Variable[]> {
        const response = await axios.get(`${API_URL}/variables/predefined`, getAuthHeaders());
        return response.data.data;
    },

    async getVariablesByType(type: string, templateId?: number): Promise<Variable[]> {
        const params = templateId ? { template_id: templateId } : {};
        const response = await axios.get(`${API_URL}/variables/type/${type}`, {
            ...getAuthHeaders(),
            params
        });
        return response.data.data;
    }
};

export default variableService;