"use client";

import { DocumentHistory } from "@/types/document";
import { format } from "date-fns";
import { es } from "date-fns/locale";
import { ClockIcon } from "@heroicons/react/24/outline";

interface DocumentHistoryProps {
    history: DocumentHistory[];
}

export const DocumentHistory = ({ history }: DocumentHistoryProps) => {
    const getActionIcon = (action: DocumentHistory["action"]) => {
        switch (action) {
            case "created":
                return "✨";
            case "updated":
                return "📝";
            case "downloaded":
                return "⬇️";
            case "viewed":
                return "👁️";
            default:
                return "📄";
        }
    };

    const getActionText = (action: DocumentHistory["action"]) => {
        switch (action) {
            case "created":
                return "Creado";
            case "updated":
                return "Actualizado";
            case "downloaded":
                return "Descargado";
            case "viewed":
                return "Visualizado";
            default:
                return action;
        }
    };

    return (
        <div className="flow-root">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Historial de Actividad</h3>
            <ul role="list" className="-mb-8">
                {history.map((event, eventIdx) => (
                    <li key={event.id}>
                        <div className="relative pb-8">
                            {eventIdx !== history.length - 1 ? (
                                <span
                                    className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                                    aria-hidden="true"
                                />
                            ) : null}
                            <div className="relative flex space-x-3">
                                <div>
                                    <span className="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center ring-8 ring-white text-lg">
                                        {getActionIcon(event.action)}
                                    </span>
                                </div>
                                <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                                    <div>
                                        <p className="text-sm text-gray-500">
                                            {event.description}{" "}
                                            <span className="font-medium text-gray-900">por {event.performedBy}</span>
                                        </p>
                                    </div>
                                    <div className="whitespace-nowrap text-right text-sm text-gray-500">
                                        <time dateTime={event.performedAt}>
                                            {format(new Date(event.performedAt), "dd MMM yyyy HH:mm", {
                                                locale: es,
                                            })}
                                        </time>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};
