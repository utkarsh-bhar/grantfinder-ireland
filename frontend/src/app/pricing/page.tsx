import Link from 'next/link';
import { PRICING } from '@/lib/constants';

export const metadata = {
  title: 'Pricing — GrantFinder Ireland',
  description: 'Affordable plans to unlock your full personalised grant report.',
};

export default function PricingPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-20">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">Simple, fair pricing</h1>
        <p className="mt-3 text-gray-500">
          The basic scan is free. Upgrade to unlock full details and application guides.
        </p>
      </div>

      <div className="mt-14 grid gap-8 md:grid-cols-3">
        {/* Free */}
        <div className="card flex flex-col">
          <h3 className="text-lg font-semibold text-gray-900">Free Scan</h3>
          <p className="mt-1 text-3xl font-bold text-gray-900">€0</p>
          <p className="mt-1 text-sm text-gray-500">Always free</p>
          <ul className="mt-6 flex-1 space-y-3">
            {[
              'Run grant eligibility scan',
              'See grant names & categories',
              'See match type (Eligible / Likely)',
              'First 3 grants with full amounts',
            ].map((f) => (
              <li key={f} className="flex items-start gap-2 text-sm text-gray-600">
                <span className="mt-0.5 text-brand-500">✓</span>
                {f}
              </li>
            ))}
          </ul>
          <Link href="/scan" className="btn-secondary mt-6 w-full text-center">
            Start Free Scan
          </Link>
        </div>

        {/* Single Report */}
        <div className="card flex flex-col border-2 border-brand-500 relative">
          <div className="absolute -top-3 left-1/2 -translate-x-1/2">
            <span className="badge bg-brand-600 text-white px-3 py-1">Most Popular</span>
          </div>
          <h3 className="text-lg font-semibold text-gray-900">{PRICING.report.name}</h3>
          <p className="mt-1 text-3xl font-bold text-gray-900">{PRICING.report.price}</p>
          <p className="mt-1 text-sm text-gray-500">One-time payment</p>
          <ul className="mt-6 flex-1 space-y-3">
            {PRICING.report.features.map((f) => (
              <li key={f} className="flex items-start gap-2 text-sm text-gray-600">
                <span className="mt-0.5 text-brand-500">✓</span>
                {f}
              </li>
            ))}
          </ul>
          <Link href="/scan" className="btn-primary mt-6 w-full text-center">
            Get My Report
          </Link>
        </div>

        {/* Premium */}
        <div className="card flex flex-col">
          <h3 className="text-lg font-semibold text-gray-900">{PRICING.monthly.name}</h3>
          <p className="mt-1 text-3xl font-bold text-gray-900">{PRICING.monthly.price}</p>
          <p className="mt-1 text-sm text-gray-500">
            or {PRICING.annual.price} <span className="text-brand-600 font-medium">{PRICING.annual.savings}</span>
          </p>
          <ul className="mt-6 flex-1 space-y-3">
            {PRICING.monthly.features.map((f) => (
              <li key={f} className="flex items-start gap-2 text-sm text-gray-600">
                <span className="mt-0.5 text-brand-500">✓</span>
                {f}
              </li>
            ))}
          </ul>
          <Link href="/scan" className="btn-secondary mt-6 w-full text-center">
            Start Premium
          </Link>
        </div>
      </div>

      {/* Feature matrix */}
      <div className="mt-16 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b">
              <th className="py-3 text-left font-medium text-gray-700">Feature</th>
              <th className="py-3 text-center font-medium text-gray-700">Free</th>
              <th className="py-3 text-center font-medium text-brand-700">Report</th>
              <th className="py-3 text-center font-medium text-gray-700">Premium</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {[
              ['Run grant scan', true, true, true],
              ['See grant names & categories', true, true, true],
              ['See match status', true, true, true],
              ['See all amounts', false, true, true],
              ['Full eligibility explanation', false, true, true],
              ['Application guide', false, true, true],
              ['Documents checklist', false, true, true],
              ['PDF report', false, true, true],
              ['Grant alerts', false, false, true],
              ['AI chat advisor', false, false, true],
              ['Deadline reminders', false, false, true],
              ['Unlimited re-scans', false, false, true],
            ].map(([feature, free, report, premium]) => (
              <tr key={feature as string}>
                <td className="py-2.5 text-gray-600">{feature as string}</td>
                <td className="py-2.5 text-center">{free ? '✓' : '—'}</td>
                <td className="py-2.5 text-center text-brand-600">{report ? '✓' : '—'}</td>
                <td className="py-2.5 text-center">{premium ? '✓' : '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
