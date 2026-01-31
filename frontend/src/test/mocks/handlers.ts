import { http, HttpResponse } from 'msw';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// モックレスポンスデータ
const mockRAGResponse = {
  answer: 'LangGraphでグラフを作成するには、StateGraphクラスを使用します。',
  sources: [
    {
      title: 'LangGraph 公式ドキュメント',
      url: 'https://langchain-ai.github.io/langgraph/',
      excerpt: 'StateGraphクラスは、状態を持つグラフを作成するためのメインクラスです。',
      relevance: 0.95,
      doc_type: 'official_docs',
    },
  ],
  code_examples: [
    {
      language: 'python',
      code: 'from langgraph.graph import StateGraph\n\ngraph = StateGraph(State)',
      description: '基本的なStateGraphの作成例',
      source_url: 'https://github.com/langchain-ai/langgraph',
    },
  ],
  confidence: 0.89,
  metadata: {
    model: 'gpt-4-turbo-preview',
    tokens_used: 1543,
    response_time: 2.34,
  },
};

const mockArchitectResponse = {
  challenge_analysis: {
    summary: 'カスタマーサポートの自動化システムの設計',
    key_requirements: [
      'FAQ自動回答',
      '複雑な問い合わせのエスカレーション',
      'Zendesk連携',
    ],
    suggested_approach: 'LangGraphの条件分岐を活用した段階的対応フロー',
    langgraph_fit_reason: 'ステート管理と条件分岐が必要なワークフローに最適',
  },
  architecture: {
    mermaid_diagram: `graph TD
    A[問い合わせ受付] --> B{FAQ検索}
    B -->|一致| C[自動回答]
    B -->|不一致| D[意図分析]`,
    node_descriptions: [
      {
        node_id: 'A',
        name: '問い合わせ受付',
        purpose: 'ユーザーからの問い合わせを受け付ける',
        description: '入力を検証して次のステップに渡す',
        inputs: ['user_query'],
        outputs: ['query_text', 'user_id'],
      },
    ],
    edge_descriptions: [
      {
        from_node: 'A',
        to_node: 'B',
        condition: null,
        description: '受付した問い合わせをFAQ検索に渡す',
      },
    ],
    state_schema: {
      query: 'str',
      faq_match: 'bool',
      complexity: 'str',
      response: 'str',
    },
  },
  code_example: {
    language: 'python',
    code: 'from langgraph.graph import StateGraph\n\ndef faq_search(state):\n    return {"faq_match": True}',
    explanation: 'カスタマーサポート自動化の基本的なLangGraphワークフロー',
  },
  business_explanation: 'FAQ検索で即座に回答できる質問を判定し、該当しない場合は複雑度を分析します。',
  implementation_notes: [
    'FAQ検索にはベクトルDBを使用することを推奨',
    'Zendesk APIの認証情報が必要',
  ],
  metadata: {
    model: 'gpt-4-turbo-preview',
    tokens_used: 3421,
    response_time: 8.76,
  },
};

const mockLearningPath = {
  learning_path: [
    {
      level: '初級',
      topics: [
        {
          id: 'basics-1',
          title: 'LangGraphの基礎',
          description: 'LangGraphの基本概念を学ぶ',
          difficulty: '初級',
          estimated_time: '30分',
          prerequisites: [],
          learning_objectives: ['StateGraphの理解', 'ノードとエッジの作成'],
          resources: [],
        },
      ],
    },
  ],
};

const mockTemplates = [
  {
    id: 'customer-support',
    name: 'カスタマーサポート自動化',
    category: 'business',
    difficulty: '中級',
    description: 'FAQ自動回答と人間へのエスカレーション',
    use_case: 'カスタマーサポート業務の効率化',
    features: ['FAQ検索', '意図分析', 'エスカレーション'],
    mermaid_diagram: 'graph TD\n    A[Start] --> B[FAQ検索]',
    code_template: 'from langgraph.graph import StateGraph',
    required_integrations: ['OpenAI API', 'Vector Database'],
    estimated_setup_time: '2-3時間',
  },
];

// MSW ハンドラー
export const handlers = [
  // RAG Query
  http.post(`${API_BASE_URL}/rag/query`, () => {
    return HttpResponse.json(mockRAGResponse);
  }),

  // Architect Generate
  http.post(`${API_BASE_URL}/architect/generate`, () => {
    return HttpResponse.json(mockArchitectResponse);
  }),

  // Learning Path
  http.get(`${API_BASE_URL}/learning-path`, () => {
    return HttpResponse.json(mockLearningPath);
  }),

  // Templates
  http.get(`${API_BASE_URL}/templates`, () => {
    return HttpResponse.json(mockTemplates);
  }),

  http.get(`${API_BASE_URL}/templates/categories`, () => {
    return HttpResponse.json({
      categories: ['business', 'data-analysis', 'automation'],
    });
  }),

  // Auth
  http.post(`${API_BASE_URL}/auth/login`, () => {
    return HttpResponse.json({
      access_token: 'mock-token',
      token_type: 'bearer',
      user: {
        username: 'testuser',
        role: 'user',
        daily_limit: 5,
      },
    });
  }),

  http.get(`${API_BASE_URL}/auth/me`, () => {
    return HttpResponse.json({
      username: 'testuser',
      role: 'user',
      daily_limit: 5,
    });
  }),

  // Usage
  http.get(`${API_BASE_URL}/usage/remaining`, () => {
    return HttpResponse.json({
      remaining: 3,
      limit: 5,
      reset_at: '2026-01-30T00:00:00Z',
    });
  }),
];
