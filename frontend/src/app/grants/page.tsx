'use client';

import { Suspense, useState, useEffect } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { grantsAPI } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';
import { CATEGORY_LABELS, CATEGORY_ICONS } from '@/types';
import type { Grant } from '@/types';

function GrantsContent() {
  const searchParams = useSearchParams();
  const categoryFilter = searchParams.get('category');
  const [grants, setGrants] = useState<Grant[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const { data } = await grantsAPI.list(1, categoryFilter || undefined);
        setGrants(data.grants || []);
      } catch {
        // API not available — show placeholder
        setGrants([]);
      }
      setLoading(false);
    };
    load();
  }, [categoryFilter]);

  const filteredGrants = searchQuery
    ? grants.filter(
        (g) =>
          g.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          g.short_description.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : grants;

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Browse all Irish grants</h1>
        <p className="mt-2 text-gray-500">
          Explore 80+ government grants, schemes, reliefs, and entitlements available in Ireland.
        </p>
      </div>

      {/* Search */}
      <div className="mb-6">
        <input
          type="text"
          className="input max-w-md"
          placeholder="Search grants..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Category filters */}
      <div className="mb-8 flex flex-wrap gap-2">
        <Link
          href="/grants"
          className={`badge px-3 py-1.5 ${!categoryFilter ? 'bg-brand-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
        >
          All
        </Link>
        {Object.entries(CATEGORY_LABELS).map(([key, label]) => (
          <Link
            key={key}
            href={`/grants?category=${key}`}
            className={`badge px-3 py-1.5 ${
              categoryFilter === key ? 'bg-brand-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {CATEGORY_ICONS[key]} {label}
          </Link>
        ))}
      </div>

      {/* Grants grid */}
      {loading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-4 w-2/3 rounded bg-gray-200" />
              <div className="mt-3 h-3 w-full rounded bg-gray-200" />
              <div className="mt-2 h-3 w-4/5 rounded bg-gray-200" />
            </div>
          ))}
        </div>
      ) : filteredGrants.length === 0 ? (
        <div className="py-20 text-center">
          <p className="text-gray-500">No grants found. Try a different search or category.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filteredGrants.map((grant) => (
            <Link key={grant.id} href={`/grants/${grant.slug}`} className="card group">
              <div className="flex items-start justify-between">
                <span className="text-lg">{CATEGORY_ICONS[grant.category] || '📋'}</span>
                {grant.max_amount && (
                  <span className="text-sm font-bold text-brand-600">
                    {formatCurrency(grant.max_amount)}
                  </span>
                )}
              </div>
              <h3 className="mt-2 text-sm font-semibold text-gray-900 group-hover:text-brand-600">
                {grant.name}
              </h3>
              <p className="mt-1 text-xs text-gray-500 line-clamp-2">{grant.short_description}</p>
              <div className="mt-3 flex items-center gap-2">
                <span className="badge bg-gray-100 text-gray-600 text-[10px]">{grant.source_organisation}</span>
                <span className="badge bg-gray-100 text-gray-600 text-[10px]">
                  {CATEGORY_LABELS[grant.category]}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default function GrantsPage() {
  return (
    <Suspense
      fallback={
        <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-4 w-2/3 rounded bg-gray-200" />
                <div className="mt-3 h-3 w-full rounded bg-gray-200" />
                <div className="mt-2 h-3 w-4/5 rounded bg-gray-200" />
              </div>
            ))}
          </div>
        </div>
      }
    >
      <GrantsContent />
    </Suspense>
  );
}
