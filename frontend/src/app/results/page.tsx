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
  const [email, setEmail] = useState('');
  const [emailStatus, setEmailStatus] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle');

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

  // Calculate totals for savings display
  const allGrants = results.categories.flatMap(c => c.grants);
  const totalAnnualSaving = allGrants.reduce((sum, g) => sum + (g.estimated_annual_saving || 0), 0);
  const backdatableGrants = allGrants.filter(g => g.estimated_backdated_saving && g.estimated_backdated_saving > 0);
  const totalBackdated = backdatableGrants.reduce((sum, g) => sum + (g.estimated_backdated_saving || 0), 0);

  const handleDownloadPDF = async () => {
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
  };

  const handleEmailReport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setEmailStatus('sending');
    try {
      await reportsAPI.emailPDF(profile, email);
      setEmailStatus('sent');
    } catch {
      setEmailStatus('error');
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      {/* ─── Total Value Banner ─────────────────────────────────────────── */}
      <div className="mb-8 rounded-2xl bg-gradient-to-br from-brand-600 to-emerald-700 p-8 text-center text-white sm:p-12">
        <p className="text-sm font-semibold uppercase tracking-wider text-brand-200">
          You could be entitled to up to
        </p>
        <p className="mt-2 text-5xl font-extrabold sm:text-6xl">
          {formatCurrency(results.total_potential_value)}
        </p>
        <p className="mt-2 text-brand-100">
          across {results.total_grants_found} grants and schemes
        </p>
      </div>

      {/* ─── Savings Stats ──────────────────────────────────────────────── */}
      <div className="mb-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="rounded-xl border border-gray-200 bg-white p-5 text-center">
          <p className="text-2xl font-bold text-brand-600">{results.total_grants_found}</p>
          <p className="mt-1 text-xs text-gray-500 uppercase tracking-wider">Grants Found</p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-5 text-center">
          <p className="text-2xl font-bold text-brand-600">{formatCurrency(results.total_potential_value)}</p>
          <p className="mt-1 text-xs text-gray-500 uppercase tracking-wider">Total Value</p>
        </div>
        {totalAnnualSaving > 0 && (
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-5 text-center">
            <p className="text-2xl font-bold text-emerald-600">{formatCurrency(totalAnnualSaving)}</p>
            <p className="mt-1 text-xs text-gray-500 uppercase tracking-wider">Est. Annual Saving</p>
          </div>
        )}
        {totalBackdated > 0 && (
          <div className="rounded-xl border border-amber-200 bg-amber-50 p-5 text-center">
            <p className="text-2xl font-bold text-amber-600">{formatCurrency(totalBackdated)}</p>
            <p className="mt-1 text-xs text-gray-500 uppercase tracking-wider">Backdated Claims</p>
          </div>
        )}
      </div>

      {/* ─── AI Summary ─────────────────────────────────────────────────── */}
      {results.summary && (
        <div className="mb-8 rounded-2xl border border-brand-200 bg-gradient-to-r from-brand-50 to-emerald-50 p-6">
          <h3 className="flex items-center gap-2 text-base font-bold text-gray-900 mb-3">
            <svg className="h-5 w-5 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456Z" />
            </svg>
            Your Personalised Analysis
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-line">{results.summary}</p>
        </div>
      )}

      {/* ─── Backdated Claims Alert ─────────────────────────────────────── */}
      {totalBackdated > 0 && (
        <div className="mb-8 rounded-2xl border-2 border-amber-300 bg-amber-50 p-6">
          <h3 className="flex items-center gap-2 text-lg font-bold text-amber-800 mb-2">
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            You may be owed up to {formatCurrency(totalBackdated)} in backdated claims
          </h3>
          <p className="text-sm text-amber-700 mb-4">
            {backdatableGrants.length} of your matched tax credits can be claimed retrospectively for up to 4 years.
            If you haven&apos;t been claiming these, Revenue may owe you a refund.
          </p>
          <div className="space-y-2">
            {backdatableGrants.slice(0, 5).map(g => (
              <div key={g.grant_id} className="flex items-center justify-between rounded-lg bg-white px-4 py-2.5 border border-amber-200">
                <div>
                  <span className="text-sm font-medium text-gray-900">{g.name}</span>
                  <span className="ml-2 text-xs text-amber-600">{formatCurrency(g.estimated_annual_saving || 0)}/yr</span>
                </div>
                <span className="text-sm font-bold text-amber-700">{formatCurrency(g.estimated_backdated_saving || 0)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

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

                    {/* Savings estimate */}
                    {grant.savings_note && (
                      <p className="mt-1 text-xs font-medium text-emerald-600">
                        {grant.savings_note}
                      </p>
                    )}

                    <p className="mt-1.5 text-xs text-gray-500 line-clamp-2">
                      {grant.short_description}
                    </p>
                    <div className="mt-3 flex items-center justify-between pt-3 border-t border-gray-100">
                      <span className="text-xs text-gray-400">{grant.source_organisation}</span>
                      <span className="text-xs font-medium text-brand-600 opacity-0 group-hover:opacity-100 transition-opacity">
                        View details &rarr;
                      </span>
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* ─── PDF Download & Email ──────────────────────────────────────── */}
      <div className="mt-10 rounded-2xl border-2 border-emerald-200 bg-gradient-to-r from-emerald-50 to-brand-50 p-8">
        <div className="text-center mb-6">
          <h3 className="text-xl font-bold text-gray-900">Get Your Full Report</h3>
          <p className="mt-1 text-sm text-gray-600">
            Includes personalised AI analysis, backdated claim amounts, Revenue myAccount claiming instructions, and all application links.
          </p>
        </div>

        <div className="flex flex-col items-center gap-6 sm:flex-row sm:justify-center">
          {/* Download PDF */}
          <button
            onClick={handleDownloadPDF}
            disabled={isDownloading}
            className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-8 py-3.5 text-sm font-semibold text-white shadow-md hover:bg-emerald-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isDownloading ? (
              <>
                <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Generating...
              </>
            ) : (
              <>
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                </svg>
                Download PDF Report
              </>
            )}
          </button>

          <span className="text-sm text-gray-400 hidden sm:inline">or</span>

          {/* Email form */}
          <form onSubmit={handleEmailReport} className="flex gap-2 w-full sm:w-auto">
            <input
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => { setEmail(e.target.value); setEmailStatus('idle'); }}
              className="input flex-1 sm:w-64"
              required
            />
            <button
              type="submit"
              disabled={emailStatus === 'sending' || emailStatus === 'sent'}
              className="rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 transition-all disabled:opacity-50 whitespace-nowrap"
            >
              {emailStatus === 'sending' ? 'Sending...' : emailStatus === 'sent' ? 'Sent!' : 'Email Report'}
            </button>
          </form>
        </div>
        {emailStatus === 'sent' && (
          <p className="mt-3 text-center text-sm text-emerald-600 font-medium">Report sent to {email}! Check your inbox.</p>
        )}
        {emailStatus === 'error' && (
          <p className="mt-3 text-center text-sm text-red-600">Failed to send. Email service may not be configured yet.</p>
        )}
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
