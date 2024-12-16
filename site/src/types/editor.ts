export interface EditorContent {
    type: "doc" | "paragraph" | "text";
    content?: EditorContent[];
    text?: string;
}

export interface EditorSection {
    id: "header" | "body" | "footer";
    content: EditorContent;
}

export interface EditorState {
    sections: {
        header: EditorContent;
        body: EditorContent;
        footer: EditorContent;
    };
    currentSection: "header" | "body" | "footer";
}
