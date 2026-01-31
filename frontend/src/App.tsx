import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Layout/Header';
import ProtectedRoute from './components/ProtectedRoute';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RAGPage from './pages/RAGPage';
import ArchitectPage from './pages/ArchitectPage';
import LearningPathPage from './pages/LearningPathPage';
import TemplatesPage from './pages/TemplatesPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[var(--color-bg-primary)]">
        <Header />

        {/* Background geometric pattern */}
        <div className="fixed inset-0 opacity-5 pointer-events-none">
          <div className="absolute top-0 right-0 w-96 h-96 bg-[var(--color-accent-primary)] rounded-full filter blur-3xl" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-[var(--color-accent-secondary)] rounded-full filter blur-3xl" />
        </div>

        {/* Main content */}
        <main className="relative pt-20 min-h-screen">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/rag"
              element={
                <ProtectedRoute>
                  <RAGPage />
                </ProtectedRoute>
              }
            />
            <Route path="/learning-path" element={<LearningPathPage />} />
            <Route path="/templates" element={<TemplatesPage />} />
            <Route
              path="/architect"
              element={
                <ProtectedRoute>
                  <ArchitectPage />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
