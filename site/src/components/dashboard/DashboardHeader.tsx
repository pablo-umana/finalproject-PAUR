"use client";

import { PlusIcon } from "@heroicons/react/24/outline";
import { useRouter } from "next/navigation";

interface DashboardHeaderProps {
    title: string;
}

export const DashboardHeader = ({ title }: DashboardHeaderProps) => {
    const router = useRouter();

    const handleNewTemplate = () => {
        router.push("/templates/new");
    };

    return (
        <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
            <button
                onClick={handleNewTemplate}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
                <PlusIcon className="h-5 w-5 mr-2" />
                Nueva Plantilla
            </button>
        </div>
    );
};
