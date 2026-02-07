import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import RAGPage from '../pages/RAGPage';
import { useRAGStore } from '../store/ragStore';

// Zustand ストアをモック化
vi.mock('../store/ragStore', () => ({
  useRAGStore: vi.fn(),
}));

describe('RAGPage', () => {
  const mockAddMessage = vi.fn();
  const mockSetLoading = vi.fn();
  const mockSetError = vi.fn();
  const mockClearMessages = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();

    // デフォルトのストア状態
    (useRAGStore as any).mockReturnValue({
      messages: [],
      isLoading: false,
      error: null,
      addMessage: mockAddMessage,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clearMessages: mockClearMessages,
    });
  });

  const renderRAGPage = () => {
    return render(
      <BrowserRouter>
        <RAGPage />
      </BrowserRouter>
    );
  };

  it('renders page title and description', () => {
    renderRAGPage();

    expect(screen.getByText(/RAG学習支援/i)).toBeInTheDocument();
    expect(screen.getByText(/LangGraphに関する質問/i)).toBeInTheDocument();
  });

  it('renders sample questions', () => {
    renderRAGPage();

    expect(screen.getByText(/LangGraphでステートグラフを作成/i)).toBeInTheDocument();
    expect(screen.getByText(/条件分岐.*の実装方法/i)).toBeInTheDocument();
  });

  it('fills input when sample question is clicked', () => {
    renderRAGPage();

    const sampleButton = screen.getByText(/LangGraphでステートグラフを作成/i);
    fireEvent.click(sampleButton);

    const input = screen.getByPlaceholderText(/LangGraphについて質問/i) as HTMLInputElement;
    expect(input.value).toContain('LangGraphでステートグラフ');
  });

  it('submits question when form is submitted', async () => {
    renderRAGPage();

    const input = screen.getByPlaceholderText(/LangGraphについて質問/i);
    const submitButton = screen.getByRole('button', { name: /質問する/i });

    fireEvent.change(input, { target: { value: 'テスト質問' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockAddMessage).toHaveBeenCalledWith({
        role: 'user',
        content: 'テスト質問',
      });
      expect(mockSetLoading).toHaveBeenCalledWith(true);
    });
  });

  it('does not submit empty question', () => {
    renderRAGPage();

    const submitButton = screen.getByRole('button', { name: /質問する/i });
    fireEvent.click(submitButton);

    expect(mockAddMessage).not.toHaveBeenCalled();
  });

  it('displays messages from store', () => {
    (useRAGStore as any).mockReturnValue({
      messages: [
        { role: 'user', content: 'ユーザーの質問' },
        { role: 'assistant', content: 'アシスタントの回答' },
      ],
      isLoading: false,
      error: null,
      addMessage: mockAddMessage,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clearMessages: mockClearMessages,
    });

    renderRAGPage();

    expect(screen.getByText('ユーザーの質問')).toBeInTheDocument();
    expect(screen.getByText('アシスタントの回答')).toBeInTheDocument();
  });

  it('displays loading state', () => {
    (useRAGStore as any).mockReturnValue({
      messages: [],
      isLoading: true,
      error: null,
      addMessage: mockAddMessage,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clearMessages: mockClearMessages,
    });

    renderRAGPage();

    expect(screen.getByText(/処理中/i)).toBeInTheDocument();
  });

  it('displays error message', () => {
    (useRAGStore as any).mockReturnValue({
      messages: [],
      isLoading: false,
      error: 'エラーメッセージ',
      addMessage: mockAddMessage,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clearMessages: mockClearMessages,
    });

    renderRAGPage();

    expect(screen.getByText(/エラーメッセージ/)).toBeInTheDocument();
  });

  it('displays sources when available', () => {
    (useRAGStore as any).mockReturnValue({
      messages: [
        {
          role: 'assistant',
          content: '回答',
          data: {
            sources: [
              {
                title: 'ソースタイトル',
                url: 'https://example.com',
                excerpt: 'ソースの抜粋',
              },
            ],
          },
        },
      ],
      isLoading: false,
      error: null,
      addMessage: mockAddMessage,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clearMessages: mockClearMessages,
    });

    renderRAGPage();

    expect(screen.getByText('ソースタイトル')).toBeInTheDocument();
  });

  it('displays code examples when available', () => {
    (useRAGStore as any).mockReturnValue({
      messages: [
        {
          role: 'assistant',
          content: '回答',
          data: {
            code_examples: [
              {
                language: 'python',
                code: 'print("Hello")',
                description: 'コードの説明',
              },
            ],
          },
        },
      ],
      isLoading: false,
      error: null,
      addMessage: mockAddMessage,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clearMessages: mockClearMessages,
    });

    renderRAGPage();

    expect(screen.getByText('コードの説明')).toBeInTheDocument();
    expect(screen.getByText(/print/i)).toBeInTheDocument();
  });
});
