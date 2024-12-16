import { DocumentList } from "@/components/documents/DocumentList";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";

export default function DashboardPage() {
    return (
        <ProtectedRoute>
            <DashboardLayout>
                <DocumentList />
            </DashboardLayout>
        </ProtectedRoute>
    );
}
