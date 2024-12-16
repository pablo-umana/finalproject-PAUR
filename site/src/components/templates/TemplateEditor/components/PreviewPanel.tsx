"use client";

import { TemplateVariable } from "@/types/template";
import { VariableSelector } from "./VariableSelector";

interface PreviewPanelProps {
    content: {
        header: string;
        body: string;
        footer: string;
    };
    onVariableSelect: (variable: TemplateVariable) => void;
}

export const PreviewPanel = ({ content, onVariableSelect }: PreviewPanelProps) => {
    return (
        <div className="w-1/3 border-l border-gray-200 bg-gray-50">
            <div className="sticky top-4">
                <div className="border-b border-gray-200">
                    <VariableSelector onSelectVariable={onVariableSelect} />
                </div>
                <div className="p-4">
                    <h3 className="text-sm font-medium text-gray-900 mb-4">Vista Previa</h3>
                    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
                        <div className="p-4 border-b border-gray-200">{content.header}</div>
                        <div className="p-4 min-h-[300px]">{content.body}</div>
                        <div className="p-4 border-t border-gray-200">{content.footer}</div>
                    </div>
                </div>
            </div>
        </div>
    );
};
