"use client";

import { useEffect, useState } from "react";
import { DocumentDetail } from "@/types/document";
import {
    getDocumentById,
    downloadDocument,
    getDocumentHistory,
    getDocumentVersions,
} from "@/services/documents/documentService";
import { format } from "date-fns";
import { es } from "date-fns/locale";
import { DocumentHistory } from "./DocumentHistory";
import { DocumentVersions } from "./DocumentVersions";

interface DocumentDetailProps {
    id: string;
    onClose: () => void;
}

export const DocumentDetail = ({ id, onClose }: DocumentDetailProps) => {
    const [document, setDocument] = useState<DocumentDetail | null>(null);
    const [loading, setLoading] = useState(true);
    const [downloading, setDownloading] = useState(false);
    const [error, setError] = useState("");
    const [history, setHistory] = useState<DocumentHistory[]>([]);
    const [versions, setVersions] = useState<DocumentVersion[]>([]);

    useEffect(() => {
        const fetchDocument = async () => {
            try {
                const [docData, versionsData] = await Promise.all([getDocumentById(id), getDocumentVersions(id)]);
                setDocument(docData);
                setVersions(versionsData);
            } catch (err) {
                setError("Error al cargar el documento");
            } finally {
                setLoading(false);
            }
        };

        fetchDocument();
    }, [id]);

    const handleDownload = async () => {
        if (!document) return;

        setDownloading(true);
        try {
            const blob = await downloadDocument(document.id);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `${document.name}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (err) {
            setError("Error al descargar el documento");
        } finally {
            setDownloading(false);
        }
    };

    if (loading) {
        return (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
                <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-2xl">
                    <p className="text-center">Cargando...</p>
                </div>
            </div>
        );
    }

    if (!document) {
        return (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
                <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-2xl">
                    <p className="text-center text-red-600">{error || "Documento no encontrado"}</p>
                    <button
                        onClick={onClose}
                        className="mt-4 w-full px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
                    >
                        Cerrar
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center overflow-y-auto">
            <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-4xl m-4">
                <div className="flex justify-between items-start">
                    <h2 className="text-2xl font-bold text-gray-900">{document.name}</h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-500">
                        <span className="sr-only">Cerrar</span>
                        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M6 18L18 6M6 6l12 12"
                            />
                        </svg>
                    </button>
                </div>

                <div className="mt-4 space-y-4">
                    <div>
                        <h3 className="text-sm font-medium text-gray-500">Detalles</h3>
                        <div className="mt-2 text-sm text-gray-900">
                            <p>
                                <span className="font-medium">Tipo:</span> {document.type}
                            </p>
                            <p>
                                <span className="font-medium">Versión:</span> {document.version}
                            </p>
                            <p>
                                <span className="font-medium">Creado por:</span> {document.createdBy}
                            </p>
                            <p>
                                <span className="font-medium">Fecha:</span>{" "}
                                {format(new Date(document.createdAt), "dd MMM yyyy", { locale: es })}
                            </p>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-sm font-medium text-gray-500">Descripción</h3>
                        <p className="mt-2 text-sm text-gray-900">{document.description}</p>
                    </div>

                    <div>
                        <h3 className="text-sm font-medium text-gray-500">Etiquetas</h3>
                        <div className="mt-2 flex flex-wrap gap-2">
                            {document.tags.map((tag) => (
                                <span
                                    key={tag}
                                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                                >
                                    {tag}
                                </span>
                            ))}
                        </div>
                    </div>

                    {error && <div className="text-red-600 text-sm">{error}</div>}

                    <div className="mt-6 flex justify-end">
                        <button
                            onClick={handleDownload}
                            disabled={downloading}
                            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                        >
                            {downloading ? "Descargando..." : "Descargar PDF"}
                        </button>
                    </div>
                </div>

                <div className="mt-8 pt-8 border-t border-gray-200">
                    <DocumentVersions versions={versions} />
                </div>
            </div>
        </div>
    );
};
