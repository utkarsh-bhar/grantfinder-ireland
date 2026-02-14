'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { grantsAPI } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';
import { CATEGORY_LABELS, CATEGORY_ICONS } from '@/types';
import type { Grant, GrantStep, GrantDocument } from '@/types';

export default function GrantDetailPage({ params }: { params: { slug: string } }) {
  const [grant, setGrant] = useState<Grant | null>(null);
  const [steps, setSteps] = useState<GrantStep[]>([]);
  const [docs, setDocs] = useState<GrantDocument[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [grantRes, stepsRes, docsRes] = await Promise.all([
          grantsAPI.get(params.slug),
          grantsAPI.steps(params.slug),
          grantsAPI.documents(params.slug),
        ]);
        setGrant(grantRes.data as any);
        setSteps(stepsRes.data || []);
        setDocs(docsRes.data || []);
      } catch {
        // API not available
      }
      setLoading(false);
    };
    load();
  }, [params.slug]);

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 w-2/3 rounded bg-gray-200" />
          <div className="h-4 w-full rounded bg-gray-200" />
          <div className="h-4 w-4/5 rounded bg-gray-200" />
        </div>
      </div>
    );
  }

  if (!grant) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-20 text-center sm:px-6">
        <h2 className="text-2xl font-bold">Grant not found</h2>
        <Link href="/grants" className="btn-primary mt-4">Browse all grants</Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
      {/* Breadcrumb */}
      <nav className="mb-6 text-sm text-gray-500">
        <Link href="/grants" className="hover:text-brand-600">Grants</Link>
        <span className="mx-2">/</span>
        <Link href={`/grants?category=${grant.category}`} className="hover:text-brand-600">
          {CATEGORY_LABELS[grant.category]}
        </Link>
        <span className="mx-2">/</span>
        <span className="text-gray-700">{grant.name}</span>
      </nav>

      {/* Header */}
      <div className="card mb-8">
        <div className="flex items-start gap-4">
          <span className="text-3xl">{CATEGORY_ICONS[grant.category] || '📋'}</span>
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-gray-900 sm:text-3xl">{grant.name}</h1>
            <p className="mt-2 text-gray-600">{grant.short_description}</p>

            <div className="mt-4 flex flex-wrap gap-3">
              {grant.max_amount && (
                <span className="badge bg-brand-100 text-brand-800 px-3 py-1 text-sm">
                  {grant.amount_description || formatCurrency(grant.max_amount)}
                </span>
              )}
              <span className="badge bg-gray-100 text-gray-600 px-3 py-1 text-sm">
                {grant.source_organisation}
              </span>
              {grant.is_means_tested && (
                <span className="badge bg-yellow-100 text-yellow-800 px-3 py-1 text-sm">
                  Means tested
                </span>
              )}
              {grant.is_always_open && (
                <span className="badge bg-green-100 text-green-800 px-3 py-1 text-sm">
                  Always open
                </span>
              )}
            </div>

            <div className="mt-6 flex gap-3">
              {grant.application_url && (
                <a href={grant.application_url} target="_blank" rel="noopener noreferrer" className="btn-primary text-sm">
                  Apply Now &rarr;
                </a>
              )}
              <a href={grant.source_url} target="_blank" rel="noopener noreferrer" className="btn-secondary text-sm">
                Official Info
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Long Description */}
      {grant.long_description && (
        <div className="card mb-8">
          <h2 className="text-lg font-semibold text-gray-900">About this grant</h2>
          <p className="mt-3 text-sm text-gray-600 leading-relaxed">{grant.long_description}</p>
        </div>
      )}

      {/* Application Steps */}
      {steps.length > 0 && (
        <div className="card mb-8">
          <h2 className="text-lg font-semibold text-gray-900">How to apply</h2>
          <div className="mt-4 space-y-4">
            {steps.map((step) => (
              <div key={step.id} className="flex gap-4">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-100 text-sm font-bold text-brand-700">
                  {step.step_number}
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-gray-900">{step.title}</h3>
                  <p className="mt-1 text-sm text-gray-500">{step.description}</p>
                  {step.url && (
                    <a href={step.url} target="_blank" rel="noopener noreferrer" className="mt-1 text-xs text-brand-600 hover:underline">
                      Visit link &rarr;
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Required Documents */}
      {docs.length > 0 && (
        <div className="card mb-8">
          <h2 className="text-lg font-semibold text-gray-900">Required documents</h2>
          <ul className="mt-4 space-y-3">
            {docs.map((doc) => (
              <li key={doc.id} className="flex items-start gap-3">
                <span className="mt-0.5 text-brand-500">
                  {doc.is_required ? '✓' : '○'}
                </span>
                <div>
                  <p className="text-sm font-medium text-gray-900">{doc.document_name}</p>
                  {doc.description && (
                    <p className="text-xs text-gray-500">{doc.description}</p>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* CTA */}
      <div className="text-center">
        <Link href="/scan" className="btn-primary">
          Check if you qualify &rarr;
        </Link>
      </div>
    </div>
  );
}
