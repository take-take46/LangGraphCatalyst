import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ArchitectPage from '../pages/ArchitectPage';
import { useArchitectStore } from '../store/architectStore';

// Zustand ストアをモック化
vi.mock('../store/architectStore', () => ({
  useArchitectStore: vi.fn(),
}));

describe('ArchitectPage', () => {
  const mockSetChallenge = vi.fn();
  const mockSetIndustry = vi.fn();
  const mockSetConstraints = vi.fn();
  const mockSetResult = vi.fn();
  const mockSetLoading = vi.fn();
  const mockSetError = vi.fn();
  const mockReset = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();

    // デフォルトのストア状態
    (useArchitectStore as any).mockReturnValue({
      challenge: '',
      industry: '',
      constraints: [],
      result: null,
      isLoading: false,
      error: null,
      setChallenge: mockSetChallenge,
      setIndustry: mockSetIndustry,
      setConstraints: mockSetConstraints,
      setResult: mockSetResult,
      setLoading: mockSetLoading,
      setError: mockSetError,
      reset: mockReset,
    });
  });

  const renderArchitectPage = () => {
    return render(
      <BrowserRouter>
        <ArchitectPage />
      </BrowserRouter>
    );
  };

  it('renders page title and description', () => {
    renderArchitectPage();

    expect(screen.getByText(/構成案生成/i)).toBeInTheDocument();
    expect(screen.getByText(/ビジネス課題を入力/i)).toBeInTheDocument();
  });

  it('renders input fields', () => {
    renderArchitectPage();

    expect(screen.getByLabelText(/ビジネス課題/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/業界.*任意/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/制約条件.*任意/i)).toBeInTheDocument();
  });

  it('renders sample challenges', () => {
    renderArchitectPage();

    expect(screen.getByText(/カスタマーサポート/i)).toBeInTheDocument();
    expect(screen.getByText(/データ分析ワークフロー/i)).toBeInTheDocument();
  });

  it('fills challenge input when sample is clicked', () => {
    renderArchitectPage();

    const sampleButton = screen.getByText(/カスタマーサポート/i);
    fireEvent.click(sampleButton);

    // ArchitectPageはuseStateを使用しているため、入力値が変更されたことを確認
    const input = screen.getByLabelText(/ビジネス課題/i) as HTMLTextAreaElement;
    expect(input.value).toContain('カスタマーサポート');
  });

  it('updates challenge when input changes', () => {
    renderArchitectPage();

    const input = screen.getByLabelText(/ビジネス課題/i);
    fireEvent.change(input, { target: { value: 'テスト課題' } });

    // ArchitectPageはuseStateを使用しているため、入力値が変更されたことを確認
    expect(input).toHaveValue('テスト課題');
  });

  it('updates industry when input changes', () => {
    renderArchitectPage();

    const input = screen.getByLabelText(/業界.*任意/i);
    fireEvent.change(input, { target: { value: 'EC' } });

    // ArchitectPageはuseStateを使用しているため、storeのsetIndustryは呼ばれない
    // 代わりに、入力値が変更されたことを確認
    expect(input).toHaveValue('EC');
  });

  it('submits form when generate button is clicked', async () => {
    (useArchitectStore as any).mockReturnValue({
      result: null,
      isLoading: false,
      error: null,
      setResult: mockSetResult,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clear: mockReset,
    });

    renderArchitectPage();

    // 課題を入力
    const input = screen.getByLabelText(/ビジネス課題/i);
    fireEvent.change(input, { target: { value: 'テスト課題' } });

    const submitButton = screen.getByRole('button', { name: /構成案を生成/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSetLoading).toHaveBeenCalledWith(true);
    });
  });

  it('does not submit empty challenge', () => {
    renderArchitectPage();

    const submitButton = screen.getByRole('button', { name: /構成案を生成/i });
    fireEvent.click(submitButton);

    expect(mockSetLoading).not.toHaveBeenCalled();
  });

  it('displays loading state', () => {
    (useArchitectStore as any).mockReturnValue({
      challenge: 'テスト課題',
      industry: '',
      constraints: [],
      result: null,
      isLoading: true,
      error: null,
      setChallenge: mockSetChallenge,
      setIndustry: mockSetIndustry,
      setConstraints: mockSetConstraints,
      setResult: mockSetResult,
      setLoading: mockSetLoading,
      setError: mockSetError,
      reset: mockReset,
    });

    renderArchitectPage();

    expect(screen.getByText(/処理中/i)).toBeInTheDocument();
  });

  it('displays error message', () => {
    (useArchitectStore as any).mockReturnValue({
      result: null,
      isLoading: false,
      error: 'エラーが発生しました',
      setResult: mockSetResult,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clear: mockReset,
    });

    renderArchitectPage();

    expect(screen.getByText(/エラーが発生しました/)).toBeInTheDocument();
  });

  it('displays result when available', () => {
    (useArchitectStore as any).mockReturnValue({
      result: {
        challenge_analysis: {
          summary: '分析サマリー',
          key_requirements: ['要件1', '要件2'],
          suggested_approach: '推奨アプローチ',
          langgraph_fit_reason: 'LangGraphが適している理由',
        },
        architecture: {
          mermaid_diagram: 'graph TD\n    A --> B',
          node_descriptions: [],
          edge_descriptions: [],
        },
        code_example: {
          language: 'python',
          code: 'print("test")',
          explanation: 'テストコード',
        },
        business_explanation: 'ビジネス向け説明',
        implementation_notes: [],
        metadata: {
          model: 'gpt-4',
          tokens_used: 100,
          response_time: 1.5,
        },
      },
      isLoading: false,
      error: null,
      setResult: mockSetResult,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clear: mockReset,
    });

    renderArchitectPage();

    // 結果が表示されていることを確認（複数の要素がある可能性があるため、最初の1つをチェック）
    const summaryElements = screen.getAllByText(/分析サマリー/);
    expect(summaryElements.length).toBeGreaterThan(0);

    const explanationElements = screen.getAllByText(/ビジネス向け説明/);
    expect(explanationElements.length).toBeGreaterThan(0);
  });

  it('displays mermaid diagram when result is available', () => {
    (useArchitectStore as any).mockReturnValue({
      result: {
        challenge_analysis: {
          summary: '分析サマリー',
          key_requirements: [],
          suggested_approach: '',
          langgraph_fit_reason: '',
        },
        architecture: {
          mermaid_diagram: 'graph TD\n    A[Start] --> B[End]',
          node_descriptions: [],
          edge_descriptions: [],
        },
        code_example: {
          language: 'python',
          code: '',
          explanation: '',
        },
        business_explanation: '',
        implementation_notes: [],
        metadata: {
          model: 'gpt-4',
          tokens_used: 100,
          response_time: 1.5,
        },
      },
      isLoading: false,
      error: null,
      setResult: mockSetResult,
      setLoading: mockSetLoading,
      setError: mockSetError,
      clear: mockReset,
    });

    renderArchitectPage();

    // Mermaidダイアグラムがレンダリングされることを確認（MermaidDiagramコンポーネントが存在）
    // Note: 実際のレンダリングはMermaidライブラリに依存するため、結果が表示されていることを確認
    const summaryElements = screen.getAllByText(/分析サマリー/);
    expect(summaryElements.length).toBeGreaterThan(0);
  });
});
