import { DocumentFilter } from "@/types/document";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

interface DocumentFiltersProps {
    filters: DocumentFilter;
    onFilterChange: (filters: DocumentFilter) => void;
}

export const DocumentFilters = ({ filters, onFilterChange }: DocumentFiltersProps) => {
    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        onFilterChange({
            ...filters,
            search: e.target.value,
        });
    };

    const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        onFilterChange({
            ...filters,
            status: e.target.value as DocumentFilter["status"],
        });
    };

    return (
        <div className="mb-6 space-y-4">
            <div className="flex gap-4">
                <div className="flex-1 relative">
                    <input
                        type="text"
                        placeholder="Buscar documentos..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value={filters.search}
                        onChange={handleSearchChange}
                    />
                    <MagnifyingGlassIcon className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                </div>
                <select
                    className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={filters.status}
                    onChange={handleStatusChange}
                >
                    <option value="">Todos los estados</option>
                    <option value="draft">Borrador</option>
                    <option value="pending">Pendiente</option>
                    <option value="completed">Completado</option>
                </select>
            </div>
        </div>
    );
};
