import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../components/UI/Button';

describe('Button Component', () => {
  it('renders with children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('renders as primary by default', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByText('Click me');
    // プライマリボタンはグラデーション背景を持つ
    expect(button).toHaveClass('bg-gradient-to-r');
    expect(button).toHaveClass('from-[var(--color-accent-primary)]');
  });

  it('renders as secondary variant', () => {
    render(<Button variant="secondary">Click me</Button>);
    const button = screen.getByText('Click me');
    // セカンダリボタンはbg-[var(--color-bg-tertiary)]を持つ
    expect(button).toHaveClass('bg-[var(--color-bg-tertiary)]');
    expect(button).toHaveClass('border');
  });

  it('renders as disabled', () => {
    render(<Button disabled>Click me</Button>);
    const button = screen.getByText('Click me');
    expect(button).toBeDisabled();
    expect(button).toHaveClass('disabled:opacity-50');
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    const button = screen.getByText('Click me');
    fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', () => {
    const handleClick = vi.fn();
    render(<Button disabled onClick={handleClick}>Click me</Button>);

    const button = screen.getByText('Click me');
    fireEvent.click(button);

    expect(handleClick).not.toHaveBeenCalled();
  });
});
