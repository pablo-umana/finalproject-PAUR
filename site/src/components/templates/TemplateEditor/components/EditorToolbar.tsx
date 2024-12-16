"use client";

import { Editor } from "@tiptap/react";
import { BoldIcon, ItalicIcon, ListBulletIcon, QueueListIcon, PhotoIcon } from "@heroicons/react/24/outline";

interface EditorToolbarProps {
    editor: Editor | null;
    onImageClick: () => void;
}

export const EditorToolbar = ({ editor, onImageClick }: EditorToolbarProps) => {
    if (!editor) {
        return null;
    }

    return (
        <div className="border-b border-gray-200 p-2 flex gap-2">
            <button
                onClick={() => editor.chain().focus().toggleBold().run()}
                className={`p-2 rounded-md tooltip ${
                    editor.isActive("bold") ? "bg-gray-100 text-blue-600" : "hover:bg-gray-100 text-gray-600"
                }`}
                title="Negrita"
            >
                <BoldIcon className="h-5 w-5" />
            </button>
            <button
                onClick={() => editor.chain().focus().toggleItalic().run()}
                className={`p-2 rounded-md tooltip ${
                    editor.isActive("italic") ? "bg-gray-100 text-blue-600" : "hover:bg-gray-100 text-gray-600"
                }`}
                title="Cursiva"
            >
                <ItalicIcon className="h-5 w-5" />
            </button>
            <button
                onClick={() => editor.chain().focus().toggleBulletList().run()}
                className={`p-2 rounded-md tooltip ${
                    editor.isActive("bulletList") ? "bg-gray-100 text-blue-600" : "hover:bg-gray-100 text-gray-600"
                }`}
                title="Lista con viñetas"
            >
                <ListBulletIcon className="h-5 w-5" />
            </button>
            <button
                onClick={() => editor.chain().focus().toggleOrderedList().run()}
                className={`p-2 rounded-md tooltip ${
                    editor.isActive("orderedList") ? "bg-gray-100 text-blue-600" : "hover:bg-gray-100 text-gray-600"
                }`}
                title="Lista numerada"
            >
                <QueueListIcon className="h-5 w-5" />
            </button>
            <div className="w-px h-6 bg-gray-200 mx-2 self-center" />
            <button
                onClick={onImageClick}
                className="p-2 rounded-md tooltip hover:bg-gray-100 text-gray-600"
                title="Insertar imagen"
            >
                <PhotoIcon className="h-5 w-5" />
            </button>
        </div>
    );
};
