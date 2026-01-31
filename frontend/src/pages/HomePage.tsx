import { Link } from 'react-router-dom';
import Card from '../components/UI/Card';

export default function HomePage() {
  const features = [
    {
      title: 'RAG学習支援',
      description: 'LangGraphに関する質問に、ソース付き・コード例付きで回答します。最新の公式情報を基にした正確な情報を提供。',
      icon: '💬',
      color: 'from-[var(--color-accent-primary)] to-blue-600',
      link: '/rag',
      stats: '公式ドキュメント + Blog + GitHub',
    },
    {
      title: '構成案生成',
      description: 'ビジネス課題を入力すると、LangGraphによる解決策を提案。Mermaid図とコード例で具体的な実装イメージを提供。',
      icon: '🏗️',
      color: 'from-[var(--color-accent-secondary)] to-purple-600',
      link: '/architect',
      stats: 'Mermaid図 + コード + 説明',
    },
    {
      title: '学習パス',
      description: '初級から上級まで、体系的なLangGraph学習カリキュラム。15のトピックで段階的にスキルアップ。',
      icon: '📚',
      color: 'from-[var(--color-accent-warm)] to-orange-600',
      link: '/learning-path',
      stats: '15トピック × 3レベル',
    },
    {
      title: 'テンプレート',
      description: 'カスタマーサポート、データ分析など、実用的なLangGraphテンプレート集。すぐに使える実装例。',
      icon: '📦',
      color: 'from-teal-500 to-cyan-600',
      link: '/templates',
      stats: '5カテゴリ × 複数テンプレート',
    },
  ];

  return (
    <div className="container mx-auto px-6 py-12">
      {/* Hero Section */}
      <div className="mb-16 animate-fade-in">
        <div className="accent-line-top mb-6" />
        <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
          LangGraph学習を
          <br />
          <span className="bg-gradient-to-r from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)] text-transparent bg-clip-text">
            加速する触媒
          </span>
        </h1>
        <p className="text-xl text-[var(--color-text-secondary)] max-w-3xl leading-relaxed">
          LangGraph Catalystは、LangGraphの学習支援とビジネス活用を促進する教育プラットフォームです。
          RAG技術による正確な情報提供、AI駆動の構成案生成、体系的な学習カリキュラムで、あなたのLangGraph習得を支援します。
        </p>

        <div className="mt-8 flex flex-wrap gap-4">
          <Link
            to="/rag"
            className="btn-primary px-6 py-3 inline-block"
          >
            今すぐ質問する →
          </Link>
          <Link
            to="/learning-path"
            className="px-6 py-3 inline-block bg-transparent border border-[var(--color-accent-primary)] text-[var(--color-accent-primary)] hover:bg-[var(--color-accent-primary)] hover:text-white transition-all font-mono font-medium"
          >
            学習を始める
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold mb-8">主要機能</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <Link
              key={feature.title}
              to={feature.link}
              className="block animate-fade-in"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <Card hover>
                <div className="flex items-start space-x-4">
                  <div className={`text-4xl p-3 bg-gradient-to-br ${feature.color} rounded-lg`}>
                    {feature.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold mb-2">{feature.title}</h3>
                    <p className="text-[var(--color-text-secondary)] mb-3 leading-relaxed">
                      {feature.description}
                    </p>
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-1 text-xs font-mono bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-accent-primary)]">
                        {feature.stats}
                      </span>
                    </div>
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Tech Stack */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold mb-8">技術スタック</h2>
        <Card hover={false}>
          <div className="grid md:grid-cols-4 gap-6">
            <div>
              <h3 className="text-lg font-bold mb-2 text-[var(--color-accent-primary)]">Backend</h3>
              <ul className="space-y-1 text-sm text-[var(--color-text-secondary)]">
                <li>• FastAPI</li>
                <li>• LangGraph</li>
                <li>• LangChain</li>
                <li>• Chroma DB</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-2 text-[var(--color-accent-primary)]">Frontend</h3>
              <ul className="space-y-1 text-sm text-[var(--color-text-secondary)]">
                <li>• React 18</li>
                <li>• TypeScript</li>
                <li>• Tailwind CSS</li>
                <li>• Zustand</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-2 text-[var(--color-accent-primary)]">LLM</h3>
              <ul className="space-y-1 text-sm text-[var(--color-text-secondary)]">
                <li>• OpenAI API</li>
                <li>• GPT-4 Turbo</li>
                <li>• Embeddings</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-2 text-[var(--color-accent-primary)]">Deploy</h3>
              <ul className="space-y-1 text-sm text-[var(--color-text-secondary)]">
                <li>• Render</li>
                <li>• Infrastructure as Code</li>
              </ul>
            </div>
          </div>
        </Card>
      </div>

      {/* Quick Start */}
      <div>
        <h2 className="text-3xl font-bold mb-8">はじめ方</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { step: '1', title: '質問する', desc: 'RAG学習支援でLangGraphについて質問' },
            { step: '2', title: '学ぶ', desc: '学習パスで基礎から体系的に学習' },
            { step: '3', title: '実装する', desc: 'テンプレートを使って実際に構築' },
          ].map((item, index) => (
            <Card key={item.step} hover={false} className="animate-fade-in" style={{ animationDelay: `${index * 100}ms` }}>
              <div className="flex items-center space-x-4 mb-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)] flex items-center justify-center text-2xl font-bold">
                  {item.step}
                </div>
                <h3 className="text-xl font-bold">{item.title}</h3>
              </div>
              <p className="text-[var(--color-text-secondary)]">{item.desc}</p>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
