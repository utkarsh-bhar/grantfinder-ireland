'use client';

import { useScanStore } from '@/stores/scanStore';
import Link from 'next/link';
import { formatCurrency, matchTypeBadge } from '@/lib/utils';
import { CATEGORY_ICONS } from '@/types';

export default function ResultsPage() {
  const { results, isScanning } = useScanStore();

  if (isScanning) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center px-4">
        <div className="animate-pulse-scale text-center">
          <span className="text-6xl">🍀</span>
          <h2 className="mt-6 text-2xl font-bold text-gray-900">Finding your grants...</h2>
          <p className="mt-2 text-gray-500">Checking 80+ grants, schemes, and reliefs against your profile.</p>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
        <span className="text-5xl">📋</span>
        <h2 className="mt-4 text-2xl font-bold text-gray-900">No results yet</h2>
        <p className="mt-2 text-gray-500">Complete the questionnaire to see your personalised grant results.</p>
        <Link href="/scan" className="btn-primary mt-6">Start Your Scan</Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      {/* ─── Total Value Banner ─────────────────────────────────────────── */}
      <div className="mb-10 rounded-2xl bg-gradient-to-br from-brand-600 to-emerald-700 p-8 text-center text-white sm:p-12">
        <p className="text-sm font-semibold uppercase tracking-wider text-brand-200">
          You could be entitled to up to
        </p>
        <p className="mt-2 text-5xl font-extrabold sm:text-6xl">
          {formatCurrency(results.total_potential_value)}
        </p>
        <p className="mt-2 text-brand-100">
          across {results.total_grants_found} grants and schemes
        </p>
        {results.summary && (
          <p className="mx-auto mt-6 max-w-2xl text-sm text-brand-100 leading-relaxed">
            {results.summary}
          </p>
        )}
      </div>

      {/* ─── Results by Category ───────────────────────────────────────── */}
      <div className="space-y-8">
        {results.categories.map((cat) => (
          <div key={cat.category}>
            <div className="mb-4 flex items-center gap-3">
              <span className="text-2xl">{CATEGORY_ICONS[cat.category] || '📋'}</span>
              <div>
                <h2 className="text-xl font-bold text-gray-900">{cat.label}</h2>
                <p className="text-sm text-gray-500">
                  {cat.count} grant{cat.count !== 1 ? 's' : ''} &middot; up to {formatCurrency(cat.total_value)}
                </p>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {cat.grants.map((grant) => {
                const badge = matchTypeBadge(grant.match_type);
                return (
                  <div
                    key={grant.grant_id}
                    className="card relative"
                  >
                    <div className="flex items-start justify-between">
                      <h3 className="pr-4 text-sm font-semibold text-gray-900 leading-snug">
                        {grant.name}
                      </h3>
                    </div>
                    <span className={`badge mt-2 ${badge.className}`}>{badge.label}</span>
                    <p className="mt-3 text-lg font-bold text-brand-600">
                      {grant.amount_description || formatCurrency(grant.max_amount)}
                    </p>
                    <p className="mt-2 text-xs text-gray-500 line-clamp-2">
                      {grant.short_description}
                    </p>
                    {grant.notes && (
                      <p className="mt-2 text-xs italic text-gray-400">{grant.notes}</p>
                    )}
                    <div className="mt-4 flex items-center gap-2">
                      <span className="text-xs text-gray-400">{grant.source_organisation}</span>
                      {grant.source_url && (
                        <a
                          href={grant.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-brand-600 hover:underline"
                        >
                          Learn more &rarr;
                        </a>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* ─── Actions ──────────────────────────────────────────────────── */}
      <div className="mt-12 rounded-2xl border-2 border-brand-200 bg-brand-50 p-8 text-center">
        <h3 className="text-xl font-bold text-gray-900">Your results are 100% free</h3>
        <p className="mt-2 text-sm text-gray-600">
          All grants, eligibility details, and application links are fully unlocked.
          Situation changed? Run a new scan anytime.
        </p>
        <div className="mt-6 flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
          <Link href="/scan" className="btn-primary">
            Re-run Scan
          </Link>
          <Link href="/grants" className="btn-secondary">
            Browse All Grants
          </Link>
        </div>
      </div>
    </div>
  );
}
