"use client";

import { useState, useEffect } from "react";
import { Document, DocumentFilter } from "@/types/document";
import { getDocuments } from "@/services/documents/documentService";
import { DocumentFilters } from "./DocumentFilters";
import { DocumentTable } from "./DocumentTable";
import { DashboardHeader } from "../dashboard/DashboardHeader";

export const DocumentList = () => {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState<DocumentFilter>({
        search: "",
    });

    useEffect(() => {
        const fetchDocuments = async () => {
            setLoading(true);
            try {
                const data = await getDocuments(filters);
                setDocuments(data);
            } catch (error) {
                console.error("Error fetching documents:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchDocuments();
    }, [filters]);

    return (
        <div className="p-6">
            <DashboardHeader title="Documentos" />
            <DocumentFilters filters={filters} onFilterChange={setFilters} />
            <DocumentTable documents={documents} loading={loading} />
        </div>
    );
};
