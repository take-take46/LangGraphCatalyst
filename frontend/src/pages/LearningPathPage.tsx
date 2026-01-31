import { useEffect, useState } from 'react';
import { useLearningStore } from '../store/learningStore';
import { learningPathApi } from '../api/learningPath';
import type { Topic } from '../types/index';
import Button from '../components/UI/Button';
import Card from '../components/UI/Card';

const LEVEL_INFO = {
  '初級': {
    title: '初級',
    icon: '🌱',
    color: 'var(--color-accent-primary)',
    description: 'LangGraphの基礎を学びます',
  },
  '中級': {
    title: '中級',
    icon: '🌿',
    color: 'var(--color-accent-secondary)',
    description: '実践的な実装パターンを習得します',
  },
  '上級': {
    title: '上級',
    icon: '🌳',
    color: 'var(--color-accent-warm)',
    description: '高度なテクニックとベストプラクティスを学びます',
  },
};

export default function LearningPathPage() {
  const { completedTopics, isTopicCompleted, markCompleted, markIncomplete } = useLearningStore();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTopic, setSelectedTopic] = useState<Topic | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<'初級' | '中級' | '上級' | null>(null);

  useEffect(() => {
    fetchTopics();
  }, []);

  const fetchTopics = async () => {
    try {
      setIsLoading(true);
      const response = await learningPathApi.getAll();
      setTopics(response.topics);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : '学習パスの取得に失敗しました');
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleComplete = (topicId: string) => {
    if (isTopicCompleted(topicId)) {
      markIncomplete(topicId);
    } else {
      markCompleted(topicId);
    }
  };

  const getLevelTopics = (level: string) => {
    return topics.filter((t) => t.level === level);
  };

  const calculateProgress = () => {
    if (topics.length === 0) return 0;
    return Math.round((completedTopics.length / topics.length) * 100);
  };

  const getLevelProgress = (level: string) => {
    const levelTopics = getLevelTopics(level);
    if (levelTopics.length === 0) return 0;
    const completed = levelTopics.filter((t) => isTopicCompleted(t.id)).length;
    return Math.round((completed / levelTopics.length) * 100);
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-6 py-12 text-center">
        <div className="text-4xl mb-4 animate-pulse">📚</div>
        <p className="text-[var(--color-text-secondary)]">学習パスを読み込んでいます...</p>
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
            <Button variant="primary" size="sm" onClick={fetchTopics} className="mt-4">
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
          <span className="bg-gradient-to-r from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)] text-transparent bg-clip-text">
            学習パス
          </span>
        </h1>
        <p className="text-xl text-[var(--color-text-secondary)] max-w-3xl leading-relaxed">
          LangGraphを体系的に学ぶためのカリキュラムです。初級から上級まで、段階的にスキルアップできます。
        </p>
      </div>

      {/* Overall Progress */}
      <Card className="mb-8 animate-fade-in">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold flex items-center">
            <span className="text-3xl mr-3">📊</span>
            全体の進捗
          </h2>
          <div className="text-right">
            <div className="text-3xl font-bold text-[var(--color-accent-primary)]">
              {calculateProgress()}%
            </div>
            <div className="text-sm text-[var(--color-text-tertiary)]">
              {completedTopics.length} / {topics.length} トピック完了
            </div>
          </div>
        </div>
        <div className="w-full h-4 bg-[var(--color-bg-tertiary)] rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)] transition-all duration-500"
            style={{ width: `${calculateProgress()}%` }}
          />
        </div>
      </Card>

      {/* Level Selection */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        {Object.entries(LEVEL_INFO).map(([level, info]) => {
          const progress = getLevelProgress(level);
          const topicCount = getLevelTopics(level).length;
          const completedCount = getLevelTopics(level).filter((t) => isTopicCompleted(t.id)).length;

          return (
            <Card
              key={level}
              className={`cursor-pointer transition-all ${
                selectedLevel === level ? 'border-2' : ''
              } animate-fade-in`}
              style={{
                borderColor: selectedLevel === level ? info.color : undefined,
                animationDelay: `${['初級', '中級', '上級'].indexOf(level) * 100}ms`,
              }}
              onClick={() => setSelectedLevel(level as typeof selectedLevel)}
            >
              <div className="text-center">
                <div className="text-5xl mb-3">{info.icon}</div>
                <h3 className="text-2xl font-bold mb-2" style={{ color: info.color }}>
                  {info.title}
                </h3>
                <p className="text-sm text-[var(--color-text-secondary)] mb-4">{info.description}</p>
                <div className="mb-2">
                  <div className="text-2xl font-bold" style={{ color: info.color }}>
                    {progress}%
                  </div>
                  <div className="text-xs text-[var(--color-text-tertiary)]">
                    {completedCount} / {topicCount} 完了
                  </div>
                </div>
                <div className="w-full h-2 bg-[var(--color-bg-tertiary)] rounded-full overflow-hidden">
                  <div
                    className="h-full transition-all duration-500"
                    style={{ width: `${progress}%`, backgroundColor: info.color }}
                  />
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Topics List */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Topics Sidebar */}
        <div className="lg:col-span-1">
          <Card className="sticky top-4">
            <h3 className="text-xl font-bold mb-4 flex items-center">
              <span className="text-2xl mr-2">📋</span>
              トピック一覧
            </h3>
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {(selectedLevel ? getLevelTopics(selectedLevel) : topics).map((topic) => {
                const completed = isTopicCompleted(topic.id);
                const levelInfo = LEVEL_INFO[topic.level as keyof typeof LEVEL_INFO];

                return (
                  <button
                    key={topic.id}
                    onClick={() => setSelectedTopic(topic)}
                    className={`w-full text-left px-4 py-3 border transition-all ${
                      selectedTopic?.id === topic.id
                        ? 'bg-[var(--color-bg-secondary)] border-[var(--color-accent-primary)]'
                        : 'bg-[var(--color-bg-tertiary)] border-[var(--color-border)] hover:border-[var(--color-accent-primary)]'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm">{levelInfo.icon}</span>
                          <span className="text-xs px-2 py-0.5 rounded" style={{ backgroundColor: `${levelInfo.color}20`, color: levelInfo.color }}>
                            {levelInfo.title}
                          </span>
                        </div>
                        <div className="text-sm font-bold text-[var(--color-text-primary)] mb-1">
                          {topic.title}
                        </div>
                        <div className="text-xs text-[var(--color-text-tertiary)]">
                          {topic.estimated_time}
                        </div>
                      </div>
                      <div className={`flex-shrink-0 ml-2 text-xl ${completed ? 'text-green-500' : 'text-[var(--color-text-tertiary)]'}`}>
                        {completed ? '✅' : '⬜'}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </Card>
        </div>

        {/* Topic Detail */}
        <div className="lg:col-span-2">
          {selectedTopic ? (
            <Card className="animate-fade-in">
              <div className="mb-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-3xl">
                        {LEVEL_INFO[selectedTopic.level as keyof typeof LEVEL_INFO].icon}
                      </span>
                      <span
                        className="px-3 py-1 text-sm font-bold rounded"
                        style={{
                          backgroundColor: `${LEVEL_INFO[selectedTopic.level as keyof typeof LEVEL_INFO].color}20`,
                          color: LEVEL_INFO[selectedTopic.level as keyof typeof LEVEL_INFO].color,
                        }}
                      >
                        {LEVEL_INFO[selectedTopic.level as keyof typeof LEVEL_INFO].title}
                      </span>
                    </div>
                    <h2 className="text-3xl font-bold mb-2">{selectedTopic.title}</h2>
                    <p className="text-[var(--color-text-secondary)] leading-relaxed">
                      {selectedTopic.description}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4 text-sm text-[var(--color-text-tertiary)]">
                  <span>⏱️ {selectedTopic.estimated_time}</span>
                  <Button
                    variant={isTopicCompleted(selectedTopic.id) ? 'outline' : 'primary'}
                    size="sm"
                    onClick={() => handleToggleComplete(selectedTopic.id)}
                  >
                    {isTopicCompleted(selectedTopic.id) ? '✅ 完了済み' : '完了にする'}
                  </Button>
                </div>
              </div>

              <div className="accent-line-top my-6" />

              {/* Learning Objectives */}
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-3 flex items-center">
                  <span className="text-2xl mr-2">🎯</span>
                  学習目標
                </h3>
                <ul className="space-y-2 text-[var(--color-text-secondary)]">
                  {selectedTopic.learning_objectives.map((obj, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-[var(--color-accent-primary)] mr-2">▸</span>
                      {obj}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Prerequisites */}
              {selectedTopic.prerequisites.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-bold mb-3 flex items-center">
                    <span className="text-2xl mr-2">📚</span>
                    前提知識
                  </h3>
                  <ul className="space-y-2 text-[var(--color-text-secondary)]">
                    {selectedTopic.prerequisites.map((prereq, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-[var(--color-accent-warm)] mr-2">•</span>
                        {prereq}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Sample Questions */}
              {selectedTopic.sample_questions.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-bold mb-3 flex items-center">
                    <span className="text-2xl mr-2">💡</span>
                    サンプル質問
                  </h3>
                  <div className="space-y-2">
                    {selectedTopic.sample_questions.map((question, idx) => (
                      <div
                        key={idx}
                        className="bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] p-3 rounded text-sm text-[var(--color-text-secondary)]"
                      >
                        <span className="text-[var(--color-accent-primary)] font-bold mr-2">Q{idx + 1}:</span>
                        {question}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Resources */}
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-3 flex items-center">
                  <span className="text-2xl mr-2">🔗</span>
                  参考資料
                </h3>
                <div className="space-y-3">
                  {selectedTopic.resources.map((resource, idx) => (
                    <a
                      key={idx}
                      href={resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] hover:border-[var(--color-accent-primary)] p-4 rounded transition-all group"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span
                              className="px-2 py-1 rounded text-xs font-bold"
                              style={{
                                backgroundColor:
                                  resource.type === 'official_docs'
                                    ? 'var(--color-accent-primary)'
                                    : resource.type === 'blog'
                                    ? 'var(--color-accent-secondary)'
                                    : 'var(--color-accent-warm)',
                                color: 'white',
                                opacity: 0.8,
                              }}
                            >
                              {resource.type === 'official_docs'
                                ? '公式ドキュメント'
                                : resource.type === 'blog'
                                ? 'ブログ'
                                : resource.type === 'video'
                                ? '動画'
                                : 'GitHub'}
                            </span>
                          </div>
                          <div className="text-sm text-[var(--color-text-secondary)] group-hover:text-[var(--color-accent-primary)] transition-colors break-all">
                            {resource.url}
                          </div>
                        </div>
                        <span className="text-[var(--color-accent-primary)] text-xl ml-3">→</span>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            </Card>
          ) : (
            <Card>
              <div className="text-center py-20 text-[var(--color-text-secondary)]">
                <div className="text-6xl mb-4">👈</div>
                <p className="text-lg">左側からトピックを選択してください</p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
