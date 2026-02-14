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
                const borderColor =
                  grant.match_type === 'eligible'
                    ? 'border-l-green-500'
                    : grant.match_type === 'likely'
                      ? 'border-l-blue-500'
                      : 'border-l-amber-500';
                return (
                  <Link
                    key={grant.grant_id}
                    href={`/grants/${grant.slug}`}
                    className={`card relative block border-l-4 ${borderColor} group hover:border-brand-300 hover:shadow-md transition-all cursor-pointer`}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span
                        className={`inline-block h-2 w-2 rounded-full ${
                          grant.match_type === 'eligible'
                            ? 'bg-green-500'
                            : grant.match_type === 'likely'
                              ? 'bg-blue-500'
                              : 'bg-amber-500'
                        }`}
                      />
                      <span
                        className={`text-xs font-medium ${
                          grant.match_type === 'eligible'
                            ? 'text-green-700'
                            : grant.match_type === 'likely'
                              ? 'text-blue-700'
                              : 'text-amber-700'
                        }`}
                      >
                        {badge.label}
                      </span>
                    </div>
                    <h3 className="text-sm font-semibold text-gray-900 leading-snug group-hover:text-brand-600 transition-colors">
                      {grant.name}
                    </h3>
                    <p className="mt-2 text-lg font-bold text-brand-600">
                      {grant.amount_description || formatCurrency(grant.max_amount)}
                    </p>
                    <p className="mt-1.5 text-xs text-gray-500 line-clamp-2">
                      {grant.short_description}
                    </p>
                    <div className="mt-3 flex items-center justify-between pt-3 border-t border-gray-100">
                      <span className="text-xs text-gray-400">{grant.source_organisation}</span>
                      <span className="text-xs font-medium text-brand-600 opacity-0 group-hover:opacity-100 transition-opacity">
                        View details →
                      </span>
                    </div>
                  </Link>
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
