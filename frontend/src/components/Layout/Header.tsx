import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import UsageLimitBadge from '../UsageLimitBadge';

export default function Header() {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-effect border-b border-gray-800">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-br from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)] transform rotate-45 group-hover:rotate-[50deg] transition-transform duration-300" />
              <div className="absolute inset-0 w-10 h-10 border-2 border-[var(--color-accent-warm)] transform -rotate-12 group-hover:rotate-[-7deg] transition-transform duration-300" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">
                LangGraph
                <span className="text-[var(--color-accent-primary)]">Catalyst</span>
              </h1>
              <p className="text-xs text-[var(--color-text-secondary)]">
                学習を加速する触媒
              </p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              to="/rag"
              className="text-sm font-mono text-[var(--color-text-secondary)] hover:text-[var(--color-accent-primary)] transition-colors relative group"
            >
              RAG学習支援
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-[var(--color-accent-primary)] group-hover:w-full transition-all duration-300" />
            </Link>
            <Link
              to="/architect"
              className="text-sm font-mono text-[var(--color-text-secondary)] hover:text-[var(--color-accent-secondary)] transition-colors relative group"
            >
              構成案生成
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-[var(--color-accent-secondary)] group-hover:w-full transition-all duration-300" />
            </Link>
            <Link
              to="/learning-path"
              className="text-sm font-mono text-[var(--color-text-secondary)] hover:text-[var(--color-accent-warm)] transition-colors relative group"
            >
              学習パス
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-[var(--color-accent-warm)] group-hover:w-full transition-all duration-300" />
            </Link>
            <Link
              to="/templates"
              className="text-sm font-mono text-[var(--color-text-secondary)] hover:text-[var(--color-accent-primary)] transition-colors relative group"
            >
              テンプレート
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-[var(--color-accent-primary)] group-hover:w-full transition-all duration-300" />
            </Link>
          </nav>

          {/* Auth Section */}
          <div className="flex items-center space-x-4">
            {isAuthenticated() ? (
              <>
                {/* Usage Limit Badge */}
                <UsageLimitBadge />

                {/* User Info */}
                <div className="hidden lg:flex items-center space-x-2 px-3 py-1 bg-[var(--color-bg-tertiary)] border border-[var(--color-border)]">
                  <span className="text-xs text-[var(--color-text-tertiary)]">👤</span>
                  <span className="text-sm font-mono text-[var(--color-text-primary)]">
                    {user?.username}
                  </span>
                  {user?.role === 'admin' && (
                    <span className="px-2 py-0.5 text-xs font-mono bg-[var(--color-accent-warm)]/20 text-[var(--color-accent-warm)] border border-[var(--color-accent-warm)]">
                      管理者
                    </span>
                  )}
                </div>

                {/* Logout Button */}
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 text-sm font-mono bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent-primary)] hover:text-[var(--color-accent-primary)] transition-all duration-300"
                >
                  ログアウト
                </button>
              </>
            ) : (
              <Link
                to="/login"
                className="px-4 py-2 text-sm font-mono bg-[var(--color-bg-tertiary)] border border-[var(--color-accent-primary)] text-[var(--color-accent-primary)] hover:bg-[var(--color-accent-primary)] hover:text-white transition-all duration-300"
              >
                ログイン
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
