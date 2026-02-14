'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/95 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <span className="text-2xl">🍀</span>
          <span className="text-xl font-bold text-brand-700">GrantFinder</span>
          <span className="hidden text-sm font-medium text-gray-400 sm:inline">.ie</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-6 md:flex">
          <Link href="/scan" className="text-sm font-medium text-gray-600 hover:text-brand-600">
            Find Grants
          </Link>
          <Link href="/grants" className="text-sm font-medium text-gray-600 hover:text-brand-600">
            Browse All
          </Link>
          <Link href="/pricing" className="text-sm font-medium text-gray-600 hover:text-brand-600">
            Pricing
          </Link>
          <Link href="/scan" className="btn-primary text-sm">
            Start Free Scan
          </Link>
        </nav>

        {/* Mobile hamburger */}
        <button
          className="md:hidden p-2"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
        >
          <svg className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            {menuOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="border-t border-gray-100 bg-white px-4 py-4 md:hidden">
          <nav className="flex flex-col gap-3">
            <Link href="/scan" className="text-sm font-medium text-gray-600" onClick={() => setMenuOpen(false)}>
              Find Grants
            </Link>
            <Link href="/grants" className="text-sm font-medium text-gray-600" onClick={() => setMenuOpen(false)}>
              Browse All
            </Link>
            <Link href="/pricing" className="text-sm font-medium text-gray-600" onClick={() => setMenuOpen(false)}>
              Pricing
            </Link>
            <Link href="/scan" className="btn-primary mt-2 text-center text-sm" onClick={() => setMenuOpen(false)}>
              Start Free Scan
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
