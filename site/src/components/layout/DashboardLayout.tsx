"use client";

import { useRouter } from "next/navigation";

interface DashboardLayoutProps {
    children: React.ReactNode;
}

export const DashboardLayout = ({ children }: DashboardLayoutProps) => {
    const router = useRouter();

    const handleLogout = () => {
        localStorage.removeItem("authToken");
        router.push("/");
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <nav className="bg-white shadow-sm">
                <div className="max-w-[95%] mx-auto px-4">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <div className="flex-shrink-0 flex items-center">
                                <img className="h-8 w-auto" src="/logo.svg" alt="Logo" />
                            </div>
                        </div>
                        <div className="flex items-center">
                            <button
                                onClick={handleLogout}
                                className="ml-4 px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                            >
                                Cerrar Sesión
                            </button>
                        </div>
                    </div>
                </div>
            </nav>
            <main className="max-w-[95%] mx-auto py-6 px-4">{children}</main>
        </div>
    );
};
