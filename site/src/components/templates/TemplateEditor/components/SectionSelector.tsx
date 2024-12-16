"use client";

interface Section {
    id: string;
    label: string;
}

interface SectionSelectorProps {
    currentSection: string;
    onSectionChange: (sectionId: string) => void;
}

export const SectionSelector = ({ currentSection, onSectionChange }: SectionSelectorProps) => {
    const sections: Section[] = [
        { id: "header", label: "Encabezado" },
        { id: "body", label: "Contenido" },
        { id: "footer", label: "Pie de página" },
    ];

    return (
        <div className="flex border-b border-gray-200">
            {sections.map((section) => (
                <button
                    key={section.id}
                    onClick={() => onSectionChange(section.id)}
                    className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px ${
                        currentSection === section.id
                            ? "border-blue-500 text-blue-600"
                            : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                    }`}
                >
                    {section.label}
                </button>
            ))}
        </div>
    );
};
