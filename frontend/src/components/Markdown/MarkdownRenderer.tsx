import ReactMarkdown from 'react-markdown';
import CodeBlock from '../CodeBlock/CodeBlock';

interface MarkdownRendererProps {
  content: string;
}

export default function MarkdownRenderer({ content }: MarkdownRendererProps) {
  return (
    <div className="prose prose-invert max-w-none">
      <ReactMarkdown
        components={{
          code({ node: _node, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '');
            const codeString = String(children).replace(/\n$/, '');
            const inline = props.inline || !match;

            if (!inline && match) {
              return <CodeBlock code={codeString} language={match[1]} />;
            }

            return (
              <code
                className="px-1.5 py-0.5 text-sm font-mono bg-[var(--color-bg-tertiary)] text-[var(--color-accent-primary)] rounded"
                {...props}
              >
                {children}
              </code>
            );
          },
          a({ href, children }) {
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[var(--color-accent-primary)] hover:text-[var(--color-accent-secondary)] underline transition-colors"
              >
                {children}
              </a>
            );
          },
          h1({ children }) {
            return <h1 className="text-3xl font-bold mb-4 mt-8 accent-line-top">{children}</h1>;
          },
          h2({ children }) {
            return <h2 className="text-2xl font-bold mb-3 mt-6">{children}</h2>;
          },
          h3({ children }) {
            return <h3 className="text-xl font-bold mb-2 mt-4">{children}</h3>;
          },
          p({ children }) {
            return <p className="mb-4 leading-relaxed">{children}</p>;
          },
          ul({ children }) {
            return <ul className="list-disc list-inside mb-4 space-y-2">{children}</ul>;
          },
          ol({ children }) {
            return <ol className="list-decimal list-inside mb-4 space-y-2">{children}</ol>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
