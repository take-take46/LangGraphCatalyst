import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodeBlockProps {
  code: string;
  language: string;
  showLineNumbers?: boolean;
}

export default function CodeBlock({ code, language, showLineNumbers = true }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group">
      <div className="absolute top-2 right-2 z-10">
        <button
          onClick={handleCopy}
          className="px-3 py-1 text-xs font-mono bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:border-[var(--color-accent-primary)] hover:text-[var(--color-accent-primary)] transition-all opacity-0 group-hover:opacity-100"
        >
          {copied ? '✓ コピー済み' : 'コピー'}
        </button>
      </div>
      <div className="absolute top-2 left-2 px-2 py-1 text-xs font-mono bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-accent-warm)]">
        {language}
      </div>
      <div className="overflow-x-auto rounded border border-[var(--color-border)] mt-0">
        <SyntaxHighlighter
          language={language}
          style={vscDarkPlus}
          showLineNumbers={showLineNumbers}
          customStyle={{
            margin: 0,
            padding: '2.5rem 1rem 1rem 1rem',
            background: '#000',
            fontSize: '0.875rem',
            fontFamily: "'IBM Plex Mono', monospace",
          }}
          lineNumberStyle={{
            color: '#4a5568',
            minWidth: '2.5em',
          }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
