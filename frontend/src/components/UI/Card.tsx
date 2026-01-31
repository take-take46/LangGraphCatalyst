import type { ReactNode, CSSProperties } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  hover?: boolean;
  style?: CSSProperties;
}

export default function Card({ children, className = '', onClick, hover = true, style }: CardProps) {
  return (
    <div
      className={`card-brutalist p-6 ${hover ? 'cursor-pointer' : ''} ${className}`}
      onClick={onClick}
      style={style}
    >
      {children}
    </div>
  );
}
