import { Document } from "@/types/document";
import { format } from "date-fns";
import { es } from "date-fns/locale";
import { useState } from "react";
import { DocumentDetail } from "./DocumentDetail";

interface DocumentTableProps {
    documents: Document[];
    loading: boolean;
}

export const DocumentTable = ({ documents, loading }: DocumentTableProps) => {
    const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(null);

    if (loading) {
        return <div className="text-center py-4">Cargando documentos...</div>;
    }

    if (documents.length === 0) {
        return <div className="text-center py-4">No se encontraron documentos</div>;
    }

    const getStatusColor = (status: Document["status"]) => {
        switch (status) {
            case "completed":
                return "bg-green-100 text-green-800";
            case "pending":
                return "bg-yellow-100 text-yellow-800";
            case "draft":
                return "bg-gray-100 text-gray-800";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };

    const getStatusText = (status: Document["status"]) => {
        switch (status) {
            case "completed":
                return "Completado";
            case "pending":
                return "Pendiente";
            case "draft":
                return "Borrador";
            default:
                return status;
        }
    };

    return (
        <>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Nombre
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Tipo
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Estado
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Creado por
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Fecha
                            </th>
                            <th className="px-6 py-3 text-right text-sm font-medium">Acciones</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {documents.map((doc) => (
                            <tr key={doc.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm font-medium text-gray-900">{doc.name}</div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm text-gray-500">{doc.type}</div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span
                                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(
                                            doc.status
                                        )}`}
                                    >
                                        {getStatusText(doc.status)}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{doc.createdBy}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {format(new Date(doc.createdAt), "dd MMM yyyy", { locale: es })}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button
                                        onClick={() => setSelectedDocumentId(doc.id)}
                                        className="text-blue-600 hover:text-blue-900"
                                    >
                                        Ver detalles
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {selectedDocumentId && (
                <DocumentDetail id={selectedDocumentId} onClose={() => setSelectedDocumentId(null)} />
            )}
        </>
    );
};
