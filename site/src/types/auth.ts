export interface LoginCredentials {
    username: string;
    password: string;
}

export interface User {
    id: number;
    username: string;
    email: string;
    roles: string[];
}

export interface LoginResponse {
    success: boolean;
    token?: string;
    user?: User;
    error?: string;
}
