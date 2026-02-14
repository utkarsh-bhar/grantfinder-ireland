'use client';

import { useState } from 'react';
import { useScanStore } from '@/stores/scanStore';
import { useProfileStore } from '@/stores/profileStore';
import Link from 'next/link';
import { formatCurrency, matchTypeBadge } from '@/lib/utils';
import { CATEGORY_ICONS } from '@/types';
import { reportsAPI } from '@/lib/api';

export default function ResultsPage() {
  const { results, isScanning } = useScanStore();
  const { profile } = useProfileStore();
  const [isDownloading, setIsDownloading] = useState(false);

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

      {/* ─── PDF Download ────────────────────────────────────────────── */}
      <div className="mt-10 rounded-2xl border-2 border-emerald-200 bg-gradient-to-r from-emerald-50 to-brand-50 p-8 text-center">
        <div className="flex items-center justify-center gap-3 mb-3">
          <svg className="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
          </svg>
          <h3 className="text-xl font-bold text-gray-900">Download Your PDF Report</h3>
        </div>
        <p className="text-sm text-gray-600 mb-5">
          Get a comprehensive, shareable PDF with all your matched grants, eligibility details, application links, and next steps.
        </p>
        <button
          onClick={async () => {
            setIsDownloading(true);
            try {
              const response = await reportsAPI.downloadPDF(profile);
              const blob = new Blob([response.data], { type: 'application/pdf' });
              const url = window.URL.createObjectURL(blob);
              const link = document.createElement('a');
              link.href = url;
              link.download = `GrantFinder_Report_${new Date().toISOString().slice(0, 10)}.pdf`;
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
              window.URL.revokeObjectURL(url);
            } catch {
              alert('There was an error generating your report. Please try again.');
            } finally {
              setIsDownloading(false);
            }
          }}
          disabled={isDownloading}
          className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-8 py-3.5 text-sm font-semibold text-white shadow-md hover:bg-emerald-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isDownloading ? (
            <>
              <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Generating Report...
            </>
          ) : (
            <>
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
              </svg>
              Download Free PDF Report
            </>
          )}
        </button>
      </div>

      {/* ─── Actions ──────────────────────────────────────────────────── */}
      <div className="mt-6 rounded-2xl border-2 border-brand-200 bg-brand-50 p-8 text-center">
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
