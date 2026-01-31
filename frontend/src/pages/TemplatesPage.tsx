import { useEffect, useState } from 'react';
import { templatesApi } from '../api/templates';
import type { Template } from '../types/index';
import Button from '../components/UI/Button';
import Card from '../components/UI/Card';
import CodeBlock from '../components/CodeBlock/CodeBlock';
import MermaidDiagram from '../components/Mermaid/MermaidDiagram';

const DIFFICULTY_INFO = {
  '初級': { label: '初級', color: 'var(--color-accent-primary)', icon: '🌱' },
  '中級': { label: '中級', color: 'var(--color-accent-secondary)', icon: '🌿' },
  '上級': { label: '上級', color: 'var(--color-accent-warm)', icon: '🌳' },
};

export default function TemplatesPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const [templatesResponse, categoriesRecord] = await Promise.all([
        templatesApi.getAll(),
        templatesApi.getCategories(),
      ]);
      setTemplates(templatesResponse.templates);
      setCategories(Object.keys(categoriesRecord));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'テンプレートの取得に失敗しました');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredTemplates = templates.filter((template) => {
    const matchesCategory = !selectedCategory || template.category === selectedCategory;
    const matchesDifficulty = !selectedDifficulty || template.difficulty === selectedDifficulty;
    const matchesSearch =
      !searchQuery ||
      template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.tags.some((tag) => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesDifficulty && matchesSearch;
  });

  const handleClearFilters = () => {
    setSelectedCategory(null);
    setSelectedDifficulty(null);
    setSearchQuery('');
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-6 py-12 text-center">
        <div className="text-4xl mb-4 animate-pulse">📦</div>
        <p className="text-[var(--color-text-secondary)]">テンプレートを読み込んでいます...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-6 py-12">
        <Card>
          <div className="text-center text-red-400">
            <div className="text-4xl mb-4">⚠️</div>
            <p>{error}</p>
            <Button variant="primary" size="sm" onClick={fetchData} className="mt-4">
              再試行
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 py-12">
      {/* Header */}
      <div className="mb-12 animate-fade-in">
        <div className="accent-line-top mb-6" />
        <h1 className="text-5xl font-bold mb-4 leading-tight">
          <span className="bg-gradient-to-r from-[var(--color-accent-warm)] to-orange-600 text-transparent bg-clip-text">
            テンプレート集
          </span>
        </h1>
        <p className="text-xl text-[var(--color-text-secondary)] max-w-3xl leading-relaxed">
          ユースケース別のLangGraphテンプレートです。Mermaid図とコード例で、すぐに実装を始められます。
        </p>
      </div>

      {/* Filters */}
      <Card className="mb-8 animate-fade-in">
        <h2 className="text-xl font-bold mb-4 flex items-center">
          <span className="text-2xl mr-2">🔍</span>
          フィルター
        </h2>

        <div className="space-y-4">
          {/* Search */}
          <div>
            <label htmlFor="search" className="block text-sm font-bold mb-2 text-[var(--color-accent-primary)]">
              検索
            </label>
            <input
              type="text"
              id="search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="タイトル、説明、タグで検索..."
              className="w-full px-4 py-2 bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-primary)] placeholder-[var(--color-text-tertiary)] focus:border-[var(--color-accent-primary)] focus:outline-none transition-colors font-mono"
            />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {/* Category Filter */}
            <div>
              <label className="block text-sm font-bold mb-2 text-[var(--color-accent-primary)]">カテゴリ</label>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSelectedCategory(null)}
                  className={`px-3 py-1 text-sm border transition-colors ${
                    selectedCategory === null
                      ? 'bg-[var(--color-accent-primary)] border-[var(--color-accent-primary)] text-white'
                      : 'bg-[var(--color-bg-tertiary)] border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent-primary)]'
                  }`}
                >
                  すべて
                </button>
                {categories.map((category) => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-3 py-1 text-sm border transition-colors ${
                      selectedCategory === category
                        ? 'bg-[var(--color-accent-primary)] border-[var(--color-accent-primary)] text-white'
                        : 'bg-[var(--color-bg-tertiary)] border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent-primary)]'
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>

            {/* Difficulty Filter */}
            <div>
              <label className="block text-sm font-bold mb-2 text-[var(--color-accent-primary)]">難易度</label>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSelectedDifficulty(null)}
                  className={`px-3 py-1 text-sm border transition-colors ${
                    selectedDifficulty === null
                      ? 'bg-[var(--color-accent-secondary)] border-[var(--color-accent-secondary)] text-white'
                      : 'bg-[var(--color-bg-tertiary)] border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent-secondary)]'
                  }`}
                >
                  すべて
                </button>
                {Object.entries(DIFFICULTY_INFO).map(([key, info]) => (
                  <button
                    key={key}
                    onClick={() => setSelectedDifficulty(key)}
                    className={`px-3 py-1 text-sm border transition-colors ${
                      selectedDifficulty === key
                        ? 'border-2 text-white'
                        : 'bg-[var(--color-bg-tertiary)] border-[var(--color-border)] text-[var(--color-text-secondary)]'
                    }`}
                    style={
                      selectedDifficulty === key
                        ? { borderColor: info.color, backgroundColor: info.color }
                        : {}
                    }
                  >
                    {info.icon} {info.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Clear Filters */}
          {(selectedCategory || selectedDifficulty || searchQuery) && (
            <Button variant="outline" size="sm" onClick={handleClearFilters}>
              フィルターをクリア
            </Button>
          )}
        </div>

        <div className="mt-4 text-sm text-[var(--color-text-tertiary)]">
          {filteredTemplates.length} 件のテンプレートが見つかりました
        </div>
      </Card>

      {/* Templates Grid/Detail View */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Templates List */}
        <div className="lg:col-span-1">
          <div className="space-y-4 max-h-[800px] overflow-y-auto">
            {filteredTemplates.length === 0 ? (
              <Card>
                <div className="text-center py-10 text-[var(--color-text-secondary)]">
                  <div className="text-4xl mb-2">🔍</div>
                  <p>条件に一致するテンプレートが見つかりませんでした</p>
                </div>
              </Card>
            ) : (
              filteredTemplates.map((template, idx) => {
                const difficultyInfo = DIFFICULTY_INFO[template.difficulty as keyof typeof DIFFICULTY_INFO];
                return (
                  <Card
                    key={template.id}
                    className={`cursor-pointer transition-all animate-fade-in ${
                      selectedTemplate?.id === template.id ? 'border-2 border-[var(--color-accent-warm)]' : ''
                    }`}
                    style={{ animationDelay: `${idx * 50}ms` }}
                    onClick={() => setSelectedTemplate(template)}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-bold text-[var(--color-text-primary)] flex-1">
                        {template.title}
                      </h3>
                      <span className="text-xl ml-2">{difficultyInfo.icon}</span>
                    </div>
                    <p className="text-sm text-[var(--color-text-secondary)] mb-3 line-clamp-2">
                      {template.description}
                    </p>
                    <div className="flex flex-wrap gap-2 mb-3">
                      <span
                        className="px-2 py-1 text-xs rounded"
                        style={{
                          backgroundColor: `${difficultyInfo.color}20`,
                          color: difficultyInfo.color,
                        }}
                      >
                        {difficultyInfo.label}
                      </span>
                      <span className="px-2 py-1 text-xs rounded bg-[var(--color-accent-primary)]/20 text-[var(--color-accent-primary)]">
                        {template.category}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {template.tags.slice(0, 3).map((tag) => (
                        <span
                          key={tag}
                          className="px-2 py-0.5 text-xs bg-[var(--color-bg-tertiary)] text-[var(--color-text-tertiary)] border border-[var(--color-border)]"
                        >
                          {tag}
                        </span>
                      ))}
                      {template.tags.length > 3 && (
                        <span className="px-2 py-0.5 text-xs text-[var(--color-text-tertiary)]">
                          +{template.tags.length - 3}
                        </span>
                      )}
                    </div>
                  </Card>
                );
              })
            )}
          </div>
        </div>

        {/* Template Detail */}
        <div className="lg:col-span-2">
          {selectedTemplate ? (
            <Card className="animate-fade-in">
              {/* Header */}
              <div className="mb-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-3xl">
                        {DIFFICULTY_INFO[selectedTemplate.difficulty as keyof typeof DIFFICULTY_INFO].icon}
                      </span>
                      <span
                        className="px-3 py-1 text-sm font-bold rounded"
                        style={{
                          backgroundColor: `${
                            DIFFICULTY_INFO[selectedTemplate.difficulty as keyof typeof DIFFICULTY_INFO].color
                          }20`,
                          color: DIFFICULTY_INFO[selectedTemplate.difficulty as keyof typeof DIFFICULTY_INFO].color,
                        }}
                      >
                        {DIFFICULTY_INFO[selectedTemplate.difficulty as keyof typeof DIFFICULTY_INFO].label}
                      </span>
                      <span className="px-3 py-1 text-sm font-bold rounded bg-[var(--color-accent-primary)]/20 text-[var(--color-accent-primary)]">
                        {selectedTemplate.category}
                      </span>
                    </div>
                    <h2 className="text-3xl font-bold mb-3">{selectedTemplate.title}</h2>
                    <p className="text-lg text-[var(--color-text-secondary)] leading-relaxed">
                      {selectedTemplate.description}
                    </p>
                  </div>
                </div>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {selectedTemplate.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 text-xs bg-[var(--color-bg-tertiary)] text-[var(--color-text-secondary)] border border-[var(--color-border)]"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="accent-line-top my-6" />

              {/* Explanation */}
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-3 flex items-center">
                  <span className="text-2xl mr-2">📖</span>
                  説明
                </h3>
                <p className="text-[var(--color-text-secondary)] leading-relaxed whitespace-pre-wrap">
                  {selectedTemplate.explanation}
                </p>
              </div>

              {/* Use Cases */}
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-3 flex items-center">
                  <span className="text-2xl mr-2">💼</span>
                  ユースケース
                </h3>
                <ul className="space-y-2 text-[var(--color-text-secondary)]">
                  {selectedTemplate.use_cases.map((useCase, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-[var(--color-accent-warm)] mr-2">▸</span>
                      {useCase}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Mermaid Diagram */}
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-3 flex items-center">
                  <span className="text-2xl mr-2">📊</span>
                  フロー図
                </h3>
                <MermaidDiagram chart={selectedTemplate.mermaid} />
              </div>

              {/* Code */}
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-3 flex items-center">
                  <span className="text-2xl mr-2">💻</span>
                  コード例
                </h3>
                <CodeBlock code={selectedTemplate.code} language="python" />
              </div>
            </Card>
          ) : (
            <Card>
              <div className="text-center py-20 text-[var(--color-text-secondary)]">
                <div className="text-6xl mb-4">👈</div>
                <p className="text-lg">左側からテンプレートを選択してください</p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
