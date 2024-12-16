import { LoginCredentials, LoginResponse } from "@/types/auth";

export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
    // Simulamos una llamada API
    return new Promise((resolve) => {
        setTimeout(() => {
            if (credentials.username === "admin" && credentials.password === "admin") {
                resolve({
                    success: true,
                    token: "mock-jwt-token",
                });
            } else {
                resolve({
                    success: false,
                    error: "Credenciales inválidas",
                });
            }
        }, 1000);
    });
};
