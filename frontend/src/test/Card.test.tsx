import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Card from '../components/UI/Card';

describe('Card Component', () => {
  it('renders children correctly', () => {
    render(
      <Card>
        <p>Test content</p>
      </Card>
    );
    expect(screen.getByText('Test content')).toBeInTheDocument();
  });

  it('applies custom className', () => {
    render(
      <Card className="custom-class">
        <p>Content</p>
      </Card>
    );
    const card = screen.getByText('Content').parentElement;
    expect(card).toHaveClass('custom-class');
  });

  it('applies default classes', () => {
    render(
      <Card>
        <p>Content</p>
      </Card>
    );
    const card = screen.getByText('Content').parentElement;
    expect(card).toHaveClass('card-brutalist', 'p-6');
  });

  it('applies cursor-pointer class when hover is true (default)', () => {
    render(
      <Card>
        <p>Content</p>
      </Card>
    );
    const card = screen.getByText('Content').parentElement;
    expect(card).toHaveClass('cursor-pointer');
  });

  it('does not apply cursor-pointer class when hover is false', () => {
    render(
      <Card hover={false}>
        <p>Content</p>
      </Card>
    );
    const card = screen.getByText('Content').parentElement;
    expect(card).not.toHaveClass('cursor-pointer');
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = vi.fn();
    render(
      <Card onClick={handleClick}>
        <p>Clickable content</p>
      </Card>
    );

    const card = screen.getByText('Clickable content').parentElement;
    fireEvent.click(card!);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not throw error when clicked without onClick handler', () => {
    render(
      <Card>
        <p>Content</p>
      </Card>
    );

    const card = screen.getByText('Content').parentElement;
    expect(() => fireEvent.click(card!)).not.toThrow();
  });
});
