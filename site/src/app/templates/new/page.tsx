import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { TemplateEditor } from "@/components/templates/TemplateEditor";

export default function NewTemplatePage() {
    return (
        <ProtectedRoute>
            <DashboardLayout>
                <TemplateEditor />
            </DashboardLayout>
        </ProtectedRoute>
    );
}
