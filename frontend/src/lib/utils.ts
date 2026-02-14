import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number | null | undefined): string {
  if (amount == null) return 'Variable';
  return new Intl.NumberFormat('en-IE', {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function matchTypeBadge(type: string): { label: string; className: string } {
  switch (type) {
    case 'eligible':
      return { label: 'Eligible', className: 'bg-green-100 text-green-800' };
    case 'likely':
      return { label: 'Likely', className: 'bg-yellow-100 text-yellow-800' };
    case 'possible':
      return { label: 'Possible', className: 'bg-blue-100 text-blue-800' };
    default:
      return { label: type, className: 'bg-gray-100 text-gray-800' };
  }
}
