"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { EditorToolbar } from "./components/EditorToolbar";
import { SectionSelector } from "./components/SectionSelector";
import EditorContent from "./components/EditorContent";
import { PreviewPanel } from "./components/PreviewPanel";
import { Editor } from "@tiptap/react";
import { saveTemplate, autoSaveTemplate, publishTemplate } from "@/services/templates/templateService";
import { Template } from "@/types/template";
import { format } from "date-fns";

interface TemplateContent {
    header: string;
    body: string;
    footer: string;
}

export const TemplateEditor = () => {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [currentSection, setCurrentSection] = useState<keyof TemplateContent>("body");
    const [editor, setEditor] = useState<Editor | null>(null);
    const [content, setContent] = useState<TemplateContent>({
        header: "",
        body: "",
        footer: "",
    });
    const [savedTemplate, setSavedTemplate] = useState<Template | null>(null);
    const [saving, setSaving] = useState(false);
    const [lastSaved, setLastSaved] = useState<Date | null>(null);

    useEffect(() => {
        if (!content.header && !content.body && !content.footer) return;

        autoSaveTemplate(
            {
                name: "Nueva Plantilla",
                content
            },
            (saved) => {
                setSavedTemplate(saved);
                setLastSaved(new Date());
            }
        );
    }, [content]);

    const handleCancel = () => {
        router.back();
    };

    const handleContentChange = (newContent: string) => {
        setContent((prev) => ({
            ...prev,
            [currentSection]: newContent,
        }));
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            const saved = await saveTemplate({
                name: "Nueva Plantilla",
                content
            });
            setSavedTemplate(saved);
            setLastSaved(new Date());
            router.push("/dashboard");
        } catch (error) {
            console.error("Error saving template:", error);
        } finally {
            setLoading(false);
        }
    };

    const handlePublish = async () => {
        if (!savedTemplate) return;
        setLoading(true);
        try {
            await publishTemplate(savedTemplate.id);
            router.push("/dashboard");
        } catch (error) {
            console.error("Error publishing template:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleVariableSelect = (variable: TemplateVariable) => {
        if (!editor) return;
        editor.chain().focus().insertContent(variable.key).run();
    };

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-900">Nueva Plantilla</h1>
                <div className="flex items-center gap-4">
                    {lastSaved && (
                        <span className="text-sm text-gray-500">
                            Guardado {format(lastSaved, "HH:mm:ss")}
                        </span>
                    )}
                    <button onClick={handleCancel}>Cancelar</button>
                    <button onClick={handleSave} disabled={loading}>
                        {loading ? "Guardando..." : "Guardar"}
                    </button>
                    {savedTemplate && (
                        <button
                            onClick={handlePublish}
                            disabled={loading}
                            className="px-4 py-2 bg-green-600 text-white rounded-md"
                        >
                            Publicar
                        </button>
                    )}
                </div>
            </div>
            <div className="bg-white shadow rounded-lg flex">
                <div className="flex-1 flex flex-col">
                    <EditorToolbar editor={editor} />
                    <SectionSelector
                        currentSection={currentSection}
                        onSectionChange={(id) => setCurrentSection(id as keyof TemplateContent)}
                    />
                    <EditorContent
                        key={currentSection}
                        section={currentSection}
                        content={content[currentSection]}
                        onChange={handleContentChange}
                        editor={editor}
                        setEditor={setEditor}
                    />
                </div>
                <PreviewPanel
                    content={content}
                    onVariableSelect={handleVariableSelect}
                />
            </div>
        </div>
    );
};
