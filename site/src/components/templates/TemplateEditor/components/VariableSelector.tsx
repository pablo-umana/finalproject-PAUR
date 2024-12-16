"use client";

import { TemplateVariable, TemplateVariableGroup } from "@/types/template";
import { useEffect, useState } from "react";
import { getVariableGroups } from "@/services/templates/variableService";

interface VariableSelectorProps {
    onSelectVariable: (variable: TemplateVariable) => void;
}

export const VariableSelector = ({ onSelectVariable }: VariableSelectorProps) => {
    const [groups, setGroups] = useState<TemplateVariableGroup[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedGroup, setSelectedGroup] = useState<string | null>(null);

    useEffect(() => {
        const loadVariables = async () => {
            try {
                const data = await getVariableGroups();
                setGroups(data);
                if (data.length > 0) {
                    setSelectedGroup(data[0].id);
                }
            } catch (error) {
                console.error("Error loading variables:", error);
            } finally {
                setLoading(false);
            }
        };

        loadVariables();
    }, []);

    if (loading) {
        return <div className="p-4 text-gray-500">Cargando variables...</div>;
    }

    const selectedGroupData = groups.find(g => g.id === selectedGroup);

    return (
        <div className="p-4 border-l border-gray-200 bg-gray-50">
            <h3 className="text-sm font-medium text-gray-900 mb-4">Variables Disponibles</h3>
            <div className="space-y-4">
                <select
                    value={selectedGroup || ""}
                    onChange={(e) => setSelectedGroup(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                    {groups.map((group) => (
                        <option key={group.id} value={group.id}>
                            {group.name}
                        </option>
                    ))}
                </select>

                <div className="space-y-2">
                    {selectedGroupData?.variables.map((variable) => (
                        <button
                            key={variable.id}
                            onClick={() => onSelectVariable(variable)}
                            className="w-full text-left px-3 py-2 hover:bg-white rounded-md text-sm flex items-center justify-between group"
                        >
                            <span className="text-gray-700">{variable.name}</span>
                            <span className="text-gray-400 group-hover:text-gray-600">{variable.key}</span>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};