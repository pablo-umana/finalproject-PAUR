"use client";

import { DocumentVersion } from "@/types/document";
import { format } from "date-fns";
import { es } from "date-fns/locale";
import { ArrowDownTrayIcon } from "@heroicons/react/24/outline";
import { downloadVersion } from "@/services/documents/documentService";
import { useState } from "react";

interface DocumentVersionsProps {
    versions: DocumentVersion[];
}

export const DocumentVersions = ({ versions }: DocumentVersionsProps) => {
    const [downloading, setDownloading] = useState<string | null>(null);

    const handleDownload = async (version: DocumentVersion) => {
        setDownloading(version.id);
        try {
            const blob = await downloadVersion(version.id);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `documento_v${version.versionNumber}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (err) {
            console.error("Error al descargar la versión:", err);
        } finally {
            setDownloading(null);
        }
    };

    return (
        <div className="flow-root">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Historial de Versiones</h3>
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
                <table className="min-w-full divide-y divide-gray-300">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Versión</th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Fecha</th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Autor</th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Cambios</th>
                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Estado</th>
                            <th className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                                <span className="sr-only">Acciones</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 bg-white">
                        {versions.map((version) => (
                            <tr key={version.id}>
                                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">
                                    v{version.versionNumber}
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    {format(new Date(version.createdAt), "dd MMM yyyy HH:mm", { locale: es })}
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                    {version.createdBy}
                                </td>
                                <td className="px-3 py-4 text-sm text-gray-500">{version.changes}</td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm">
                                    <span
                                        className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                                            version.status === "active"
                                                ? "bg-green-100 text-green-800"
                                                : "bg-gray-100 text-gray-800"
                                        }`}
                                    >
                                        {version.status === "active" ? "Activa" : "Archivada"}
                                    </span>
                                </td>
                                <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                    <button
                                        onClick={() => handleDownload(version)}
                                        disabled={downloading === version.id}
                                        className="text-blue-600 hover:text-blue-900 inline-flex items-center gap-1"
                                    >
                                        <ArrowDownTrayIcon className="h-4 w-4" />
                                        {downloading === version.id ? "Descargando..." : "Descargar"}
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
