import { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

interface MermaidDiagramProps {
  chart: string;
}

export default function MermaidDiagram({ chart }: MermaidDiagramProps) {
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'dark',
      themeVariables: {
        primaryColor: '#0ea5e9',
        primaryTextColor: '#e4e7eb',
        primaryBorderColor: '#2d3748',
        lineColor: '#0ea5e9',
        secondaryColor: '#a855f7',
        tertiaryColor: '#1e2530',
        background: '#151922',
        mainBkg: '#151922',
        secondBkg: '#1e2530',
        tertiaryBkg: '#0a0e14',
        textColor: '#e4e7eb',
        fontSize: '14px',
        fontFamily: "'IBM Plex Mono', monospace",
      },
    });

    if (elementRef.current) {
      elementRef.current.innerHTML = chart;
      mermaid.contentLoaded();
    }
  }, [chart]);

  return (
    <div className="bg-[var(--color-bg-secondary)] border border-[var(--color-border)] rounded p-6 overflow-x-auto">
      <div ref={elementRef} className="mermaid flex justify-center" />
    </div>
  );
}
