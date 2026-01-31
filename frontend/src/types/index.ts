// RAG Types
export interface RAGQueryRequest {
  question: string;
  k?: number;
  include_sources?: boolean;
  include_code_examples?: boolean;
}

export interface Source {
  title: string;
  url: string;
  excerpt: string;
  relevance: number;
  doc_type: string;
}

export interface CodeExample {
  language: string;
  code: string;
  description: string;
  source_url?: string;
}

export interface RAGQueryResponse {
  answer: string;
  sources: Source[];
  code_examples: CodeExample[];
  confidence: number;
  metadata: {
    model: string;
    tokens_used: number;
    response_time: number;
  };
}

// Architect Types
export interface ArchitectRequest {
  business_challenge: string;
  industry?: string;
  constraints?: string[];
}

export interface NodeDescription {
  node_id: string;
  name: string;
  purpose: string;
  description: string;
  inputs: string[];
  outputs: string[];
}

export interface EdgeDescription {
  from_node: string;
  to_node: string;
  condition?: string;
  description: string;
}

export interface Architecture {
  mermaid_diagram: string;
  node_descriptions: NodeDescription[];
  edge_descriptions: EdgeDescription[];
  state_schema: Record<string, unknown>;
}

export interface ArchitectResponse {
  challenge_analysis: {
    summary: string;
    key_requirements: string[];
    suggested_approach: string;
    langgraph_fit_reason: string;
  };
  architecture: Architecture;
  code_example: {
    language: string;
    code: string;
    explanation: string;
  };
  business_explanation: string;
  implementation_notes: string[];
  metadata: {
    model: string;
    tokens_used: number;
    response_time: number;
  };
}

// Learning Path Types
export interface Topic {
  id: string;
  level: string;
  order: number;
  title: string;
  description: string;
  learning_objectives: string[];
  sample_questions: string[];
  prerequisites: string[];
  estimated_time: string;
  resources: Array<{
    type: string;
    url: string;
  }>;
}

export interface LearningPathResponse {
  topics: Topic[];
  total_count: number;
  levels: Record<string, number>;
}

export interface ProgressResponse {
  total_progress: number;
  completed_count: number;
  total_count: number;
  levels: Record<string, {
    progress: number;
    completed: number;
    total: number;
  }>;
}

// Template Types
export interface Template {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: string;
  code: string;
  mermaid: string;
  explanation: string;
  use_cases: string[];
  tags: string[];
}

export interface TemplatesListResponse {
  templates: Template[];
  total_count: number;
  categories: Record<string, number>;
  difficulties: Record<string, number>;
}
