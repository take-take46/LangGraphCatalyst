import { useState, useRef, useEffect } from 'react';
import { useRAGStore } from '../store/ragStore';
import { ragApi } from '../api/rag';
import Button from '../components/UI/Button';
import Card from '../components/UI/Card';
import CodeBlock from '../components/CodeBlock/CodeBlock';
import MarkdownRenderer from '../components/Markdown/MarkdownRenderer';

const SAMPLE_QUESTIONS = [
  'LangGraphでステートグラフを作成する方法を教えてください',
  '条件分岐(conditional edge)の実装方法は？',
  'LangGraphとLangChainの違いは何ですか？',
  'Human-in-the-loopの実装例を教えてください',
];

export default function RAGPage() {
  const { messages, isLoading, error, addMessage, setLoading, setError, clearMessages } = useRAGStore();
  const [question, setQuestion] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    const userQuestion = question.trim();
    setQuestion('');
    setError(null);

    // Add user message
    addMessage({
      role: 'user',
      content: userQuestion,
    });

    // Query RAG
    setLoading(true);
    try {
      const response = await ragApi.query({
        question: userQuestion,
        k: 5,
        include_sources: true,
        include_code_examples: true,
      });

      // Add assistant message with full response data
      addMessage({
        role: 'assistant',
        content: response.answer,
        data: response,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : '回答の生成に失敗しました');
      addMessage({
        role: 'assistant',
        content: 'エラーが発生しました。もう一度お試しください。',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSampleQuestion = (sampleQuestion: string) => {
    setQuestion(sampleQuestion);
  };

  return (
    <div className="container mx-auto px-6 py-12">
      {/* Header */}
      <div className="mb-12 animate-fade-in">
        <div className="accent-line-top mb-6" />
        <h1 className="text-5xl font-bold mb-4 leading-tight">
          <span className="bg-gradient-to-r from-[var(--color-accent-primary)] to-blue-600 text-transparent bg-clip-text">
            RAG学習支援
          </span>
        </h1>
        <p className="text-xl text-[var(--color-text-secondary)] max-w-3xl leading-relaxed">
          LangGraphに関する質問に、公式ドキュメント・ブログ・GitHubから最新の情報を基に、ソース付き・コード例付きで回答します。
        </p>

        {/* Clear Chat Button */}
        {messages.length > 0 && (
          <Button
            variant="outline"
            size="sm"
            onClick={clearMessages}
            className="mt-4"
          >
            会話をクリア
          </Button>
        )}
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Main Chat Area */}
        <div className="lg:col-span-2">
          {/* Messages */}
          <Card className="mb-6 min-h-[500px] max-h-[600px] overflow-y-auto">
            {messages.length === 0 ? (
              <div className="text-center py-20 text-[var(--color-text-secondary)]">
                <div className="text-6xl mb-4">💬</div>
                <p className="text-lg">質問を入力するか、サンプル質問を選択してください</p>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`animate-fade-in ${
                      message.role === 'user' ? 'text-right' : ''
                    }`}
                  >
                    {/* User Message */}
                    {message.role === 'user' && (
                      <div className="inline-block max-w-[80%] text-left">
                        <div className="bg-[var(--color-bg-tertiary)] border border-[var(--color-accent-primary)] p-4 rounded">
                          <p className="text-[var(--color-text-primary)]">{message.content}</p>
                        </div>
                        <div className="text-xs text-[var(--color-text-tertiary)] mt-1">
                          {new Date(message.timestamp).toLocaleTimeString('ja-JP')}
                        </div>
                      </div>
                    )}

                    {/* Assistant Message */}
                    {message.role === 'assistant' && (
                      <div className="space-y-4">
                        <div className="flex items-start space-x-3">
                          <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)] rounded flex items-center justify-center text-white font-bold">
                            AI
                          </div>
                          <div className="flex-1">
                            <div className="bg-[var(--color-bg-secondary)] border border-[var(--color-border)] p-4 rounded">
                              <MarkdownRenderer content={message.content} />
                            </div>
                            <div className="text-xs text-[var(--color-text-tertiary)] mt-1">
                              {new Date(message.timestamp).toLocaleTimeString('ja-JP')}
                              {message.data?.metadata && (
                                <span className="ml-4">
                                  • {message.data.metadata.tokens_used} tokens
                                  • {message.data.metadata.response_time.toFixed(2)}s
                                  • 信頼度: {(message.data.confidence * 100).toFixed(0)}%
                                </span>
                              )}
                            </div>

                            {/* Sources */}
                            {message.data?.sources && message.data.sources.length > 0 && (
                              <div className="mt-4">
                                <h4 className="text-sm font-bold mb-2 text-[var(--color-accent-warm)]">
                                  📚 参照ソース
                                </h4>
                                <div className="space-y-2">
                                  {message.data.sources.map((source, idx) => (
                                    <div
                                      key={idx}
                                      className="bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] p-3 rounded text-sm"
                                    >
                                      <a
                                        href={source.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-[var(--color-accent-primary)] hover:text-[var(--color-accent-secondary)] font-bold transition-colors"
                                      >
                                        {source.title}
                                      </a>
                                      <p className="text-[var(--color-text-secondary)] mt-1 text-xs">
                                        {source.excerpt}
                                      </p>
                                      <div className="flex items-center justify-between mt-2">
                                        <span className="text-xs text-[var(--color-text-tertiary)]">
                                          {source.doc_type}
                                        </span>
                                        <span className="text-xs text-[var(--color-accent-warm)]">
                                          関連度: {(source.relevance * 100).toFixed(0)}%
                                        </span>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Code Examples */}
                            {message.data?.code_examples && message.data.code_examples.length > 0 && (
                              <div className="mt-4">
                                <h4 className="text-sm font-bold mb-2 text-[var(--color-accent-warm)]">
                                  💻 コード例
                                </h4>
                                <div className="space-y-4">
                                  {message.data.code_examples.map((example, idx) => (
                                    <div key={idx}>
                                      <p className="text-sm text-[var(--color-text-secondary)] mb-2">
                                        {example.description}
                                      </p>
                                      <CodeBlock
                                        code={example.code}
                                        language={example.language}
                                      />
                                      {example.source_url && (
                                        <a
                                          href={example.source_url}
                                          target="_blank"
                                          rel="noopener noreferrer"
                                          className="text-xs text-[var(--color-accent-primary)] hover:text-[var(--color-accent-secondary)] transition-colors"
                                        >
                                          ソースを見る →
                                        </a>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex items-start space-x-3 animate-fade-in">
                    <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)] rounded flex items-center justify-center text-white font-bold">
                      AI
                    </div>
                    <div className="bg-[var(--color-bg-secondary)] border border-[var(--color-border)] p-4 rounded">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-[var(--color-accent-primary)] rounded-full animate-pulse" />
                        <div className="w-2 h-2 bg-[var(--color-accent-primary)] rounded-full animate-pulse" style={{ animationDelay: '0.2s' }} />
                        <div className="w-2 h-2 bg-[var(--color-accent-primary)] rounded-full animate-pulse" style={{ animationDelay: '0.4s' }} />
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            )}
          </Card>

          {/* Input Form */}
          <Card>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="question" className="block text-sm font-bold mb-2 text-[var(--color-accent-primary)]">
                  質問を入力
                </label>
                <textarea
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="LangGraphについて質問してください..."
                  className="w-full px-4 py-3 bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-primary)] placeholder-[var(--color-text-tertiary)] focus:border-[var(--color-accent-primary)] focus:outline-none transition-colors font-mono"
                  rows={3}
                  disabled={isLoading}
                />
              </div>

              {error && (
                <div className="p-3 bg-red-900/20 border border-red-500/50 text-red-400 text-sm">
                  ⚠️ {error}
                </div>
              )}

              <Button
                type="submit"
                variant="primary"
                size="lg"
                className="w-full"
                isLoading={isLoading}
                disabled={!question.trim() || isLoading}
              >
                {isLoading ? '回答を生成中...' : '質問する'}
              </Button>
            </form>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1">
          {/* Sample Questions */}
          <Card className="mb-6">
            <h3 className="text-xl font-bold mb-4 flex items-center">
              <span className="text-2xl mr-2">💡</span>
              サンプル質問
            </h3>
            <div className="space-y-2">
              {SAMPLE_QUESTIONS.map((sample, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSampleQuestion(sample)}
                  disabled={isLoading}
                  className="w-full text-left px-4 py-3 bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent-primary)] hover:text-[var(--color-text-primary)] transition-all text-sm disabled:opacity-50"
                >
                  {sample}
                </button>
              ))}
            </div>
          </Card>

          {/* Info Card */}
          <Card hover={false}>
            <h3 className="text-lg font-bold mb-3 text-[var(--color-accent-primary)]">
              📖 データソース
            </h3>
            <ul className="space-y-2 text-sm text-[var(--color-text-secondary)]">
              <li>• LangGraph公式ドキュメント</li>
              <li>• LangChain Blog</li>
              <li>• GitHub (langchain-ai/langgraph)</li>
            </ul>
            <div className="mt-4 pt-4 border-t border-[var(--color-border)]">
              <h4 className="text-sm font-bold mb-2 text-[var(--color-accent-warm)]">
                回答に含まれる情報
              </h4>
              <ul className="space-y-1 text-xs text-[var(--color-text-tertiary)]">
                <li>✓ 公式ドキュメントからの引用</li>
                <li>✓ 実装コード例</li>
                <li>✓ 参照ソースURL</li>
                <li>✓ 信頼度スコア</li>
              </ul>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
