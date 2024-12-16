"use client";

import {
    ArrowsPointingOutIcon,
    Bars3BottomLeftIcon,
    Bars3BottomRightIcon,
    Bars3Icon,
    BoldIcon,
    ItalicIcon,
    ListBulletIcon,
    PhotoIcon,
    QueueListIcon,
    TableCellsIcon
} from "@heroicons/react/24/solid";
import BubbleMenuExtension from "@tiptap/extension-bubble-menu";
import Image from "@tiptap/extension-image";
import Placeholder from "@tiptap/extension-placeholder";
import TextAlign from '@tiptap/extension-text-align';
import { BubbleMenu, EditorContent as TiptapContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Table from '@tiptap/extension-table';
import TableRow from '@tiptap/extension-table-row';
import TableCell from '@tiptap/extension-table-cell';
import TableHeader from '@tiptap/extension-table-header';
import { useEffect, useRef, useState } from "react";
import { VariableSelector } from "./VariableSelector";
import { TemplateVariable } from "@/types/template";

interface EditorContentProps {
    section: string;
    content: string;
    onChange: (content: string) => void;
    editor: Editor | null;
    setEditor: (editor: Editor | null) => void;
}

const EditorContent = (props: EditorContentProps) => {
    const [isMounted, setIsMounted] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const editor = useEditor({
        immediatelyRender: false,
        extensions: [
            StarterKit,
            Placeholder.configure({
                placeholder: `Edita el contenido del ${props.section} aquí...`,
                emptyEditorClass: "is-editor-empty",
            }),
            BubbleMenuExtension,
            Image.configure({
                HTMLAttributes: {
                    class: 'max-w-full h-auto',
                },
            }),
            TextAlign.configure({
                types: ['heading', 'paragraph', 'image', 'table'],
                alignments: ['left', 'center', 'right', 'justify'],
            }),
            Table.configure({
                resizable: true,
                HTMLAttributes: {
                    class: 'border-collapse table-auto w-full',
                },
            }),
            TableRow,
            TableCell,
            TableHeader,
        ],
        content: props.content || "<p></p>",
        onUpdate: ({ editor }) => {
            props.onChange(editor.getHTML());
        },
        editorProps: {
            attributes: {
                class: "prose prose-sm sm:prose lg:prose-lg xl:prose-xl focus:outline-none min-h-[200px] w-full max-w-none",
            },
        },
    });

    useEffect(() => {
        props.setEditor(editor);
    }, [editor, props.setEditor]);

    const handleImageUpload = async (file: File) => {
        if (!editor) return;

        if (file.size > 1024 * 1024) {
            alert('La imagen no debe superar 1MB');
            return;
        }

        if (!file.type.startsWith('image/')) {
            alert('Solo se permiten archivos de imagen');
            return;
        }

        try {
            const reader = new FileReader();
            reader.onload = (e) => {
                if (typeof e.target?.result === 'string') {
                    editor
                        .chain()
                        .focus()
                        .setImage({ src: e.target.result, alt: file.name })
                        .run();
                }
            };
            reader.readAsDataURL(file);
        } catch (error) {
            console.error('Error al cargar la imagen:', error);
            alert('Error al cargar la imagen');
        }
    };

    const handleImageClick = () => {
        fileInputRef.current?.click();
    };

    const insertTable = (cols: number) => {
        if (!editor) return;
        editor.chain().focus().insertTable({ rows: 1, cols }).run();
    };

    const handleVariableSelect = (variable: TemplateVariable) => {
        if (!editor) return;
        editor.chain().focus().insertContent(variable.key).run();
    };

    useEffect(() => {
        setIsMounted(true);
    }, []);

    if (!isMounted || !editor) {
        return (
            <div className="flex-1 p-4">
                <div className="border border-gray-200 rounded-lg min-h-[200px] p-4">
                    <p className="text-gray-400">Cargando editor...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1">
            <div className="border border-gray-200 rounded-lg overflow-hidden bg-white">
                <div className="min-h-[200px] w-full relative">
                    <input
                        type="file"
                        ref={fileInputRef}
                        className="hidden"
                        accept="image/*"
                        onChange={(e) => {
                            const file = e.target.files?.[0];
                            if (file) handleImageUpload(file);
                            e.target.value = "";
                        }}
                    />
                    {editor && (
                        <BubbleMenu
                            editor={editor}
                            tippyOptions={{ duration: 100 }}
                            className="bg-white shadow-lg border border-gray-200 rounded-lg flex overflow-hidden"
                        >
                            <button
                                onClick={() => editor.chain().focus().toggleBold().run()}
                                className={`p-2 hover:bg-gray-100 ${
                                    editor.isActive("bold") ? "text-blue-600 bg-gray-100" : "text-gray-600"
                                }`}
                            >
                                <BoldIcon className="w-4 h-4" />
                            </button>
                            <button
                                onClick={() => editor.chain().focus().toggleItalic().run()}
                                className={`p-2 hover:bg-gray-100 ${
                                    editor.isActive("italic") ? "text-blue-600 bg-gray-100" : "text-gray-600"
                                }`}
                            >
                                <ItalicIcon className="w-4 h-4" />
                            </button>
                            <div className="w-px h-4 bg-gray-200 my-auto mx-1" />
                            <button
                                onClick={() => editor.chain().focus().setTextAlign("left").run()}
                                className={`p-2 hover:bg-gray-100 ${
                                    editor.isActive({ textAlign: "left" })
                                        ? "text-blue-600 bg-gray-100"
                                        : "text-gray-600"
                                }`}
                            >
                                <Bars3BottomLeftIcon className="w-4 h-4" />
                            </button>
                            <button
                                onClick={() => editor.chain().focus().setTextAlign("center").run()}
                                className={`p-2 hover:bg-gray-100 ${
                                    editor.isActive({ textAlign: "center" })
                                        ? "text-blue-600 bg-gray-100"
                                        : "text-gray-600"
                                }`}
                            >
                                <Bars3Icon className="w-4 h-4" />
                            </button>
                            <button
                                onClick={() => editor.chain().focus().setTextAlign("right").run()}
                                className={`p-2 hover:bg-gray-100 ${
                                    editor.isActive({ textAlign: "right" })
                                        ? "text-blue-600 bg-gray-100"
                                        : "text-gray-600"
                                }`}
                            >
                                <Bars3BottomRightIcon className="w-4 h-4" />
                            </button>
                            <button
                                onClick={() => editor.chain().focus().setTextAlign("justify").run()}
                                className={`p-2 hover:bg-gray-100 ${
                                    editor.isActive({ textAlign: "justify" })
                                        ? "text-blue-600 bg-gray-100"
                                        : "text-gray-600"
                                }`}
                            >
                                <ArrowsPointingOutIcon className="w-4 h-4" />
                            </button>
                            <div className="w-px h-4 bg-gray-200 my-auto mx-1" />
                            <button
                                onClick={() => editor.chain().focus().toggleBulletList().run()}
                                className={`p-2 hover:bg-gray-100 ${
                                    editor.isActive("bulletList") ? "text-blue-600 bg-gray-100" : "text-gray-600"
                                }`}
                            >
                                <ListBulletIcon className="w-4 h-4" />
                            </button>
                            <button
                                onClick={() => editor.chain().focus().toggleOrderedList().run()}
                                className={`p-2 hover:bg-gray-100 ${
                                    editor.isActive("orderedList") ? "text-blue-600 bg-gray-100" : "text-gray-600"
                                }`}
                            >
                                <QueueListIcon className="w-4 h-4" />
                            </button>
                            <div className="w-px h-4 bg-gray-200 my-auto mx-1" />
                            <button
                                onClick={handleImageClick}
                                className="p-2 hover:bg-gray-100 text-gray-600"
                                title="Insertar imagen"
                            >
                                <PhotoIcon className="w-4 h-4" />
                            </button>
                            <div className="relative">
                                <button
                                    onClick={() => insertTable(2)}
                                    className="p-2 hover:bg-gray-100 text-gray-600"
                                    title="Insertar tabla"
                                >
                                    <TableCellsIcon className="w-4 h-4" />
                                </button>
                                <div className="absolute hidden hover:flex group-hover:flex flex-col bg-white shadow-lg border border-gray-200 rounded-lg p-2 z-50 top-full left-0 min-w-[120px]">
                                    <button
                                        onClick={() => insertTable(2)}
                                        className="px-4 py-2 hover:bg-gray-100 text-sm text-left"
                                    >
                                        2 columnas
                                    </button>
                                    <button
                                        onClick={() => insertTable(3)}
                                        className="px-4 py-2 hover:bg-gray-100 text-sm text-left"
                                    >
                                        3 columnas
                                    </button>
                                </div>
                            </div>
                        </BubbleMenu>
                    )}
                    <TiptapContent editor={editor} />
                </div>
            </div>
        </div>
    );
};

export default EditorContent;
