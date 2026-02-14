import Link from 'next/link';
import { CATEGORY_LABELS, CATEGORY_ICONS } from '@/types';

export default function HomePage() {
  const categories = Object.entries(CATEGORY_LABELS).slice(0, 8);

  return (
    <>
      {/* ─── Hero ────────────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden bg-gradient-to-br from-brand-600 via-brand-700 to-emerald-800">
        <div className="absolute inset-0 bg-[url('/images/grid.svg')] opacity-10" />
        <div className="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 sm:py-28 lg:py-36">
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">
              Discover every grant you&apos;re entitled to in Ireland
            </h1>
            <p className="mt-6 text-lg text-brand-100 sm:text-xl">
              Answer a few questions about your situation. Our engine checks 80+ grants, schemes, and
              reliefs to find what you qualify for — housing, energy, business, welfare, education, and
              more.
            </p>
            <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
              <Link href="/scan" className="w-full sm:w-auto rounded-xl bg-white px-8 py-4 text-lg font-bold text-brand-700 shadow-lg transition hover:bg-brand-50 hover:shadow-xl">
                Find My Grants — Free
              </Link>
              <Link href="/grants" className="text-sm font-medium text-brand-100 underline underline-offset-4 hover:text-white">
                Browse all grants
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Social Proof ────────────────────────────────────────────────── */}
      <section className="border-b border-gray-200 bg-white py-8">
        <div className="mx-auto max-w-5xl px-4 text-center sm:px-6">
          <p className="text-lg font-medium text-gray-600">
            Irish residents are missing an average of <span className="font-bold text-brand-600">€8,700</span> in
            grants and entitlements each year.
          </p>
        </div>
      </section>

      {/* ─── How It Works ────────────────────────────────────────────────── */}
      <section className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6">
          <h2 className="text-center text-3xl font-bold text-gray-900 sm:text-4xl">
            How it works
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-gray-500">
            Three simple steps. Under 3 minutes. Completely free to start.
          </p>

          <div className="mt-14 grid gap-8 md:grid-cols-3">
            {[
              { step: '1', icon: '📋', title: 'Answer 15 quick questions', desc: 'Tell us about your home, family, work, and situation. No personal data needed — just your circumstances.' },
              { step: '2', icon: '🔍', title: 'We check 80+ grants', desc: 'Our rules engine evaluates your answers against every known Irish grant, scheme, relief, and entitlement.' },
              { step: '3', icon: '📊', title: 'Get your personalised report', desc: 'See exactly what you qualify for, how much you can get, and step-by-step guides on how to apply.' },
            ].map((item) => (
              <div key={item.step} className="card text-center">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-brand-50 text-3xl">
                  {item.icon}
                </div>
                <div className="mt-2 inline-flex h-6 w-6 items-center justify-center rounded-full bg-brand-600 text-xs font-bold text-white">
                  {item.step}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900">{item.title}</h3>
                <p className="mt-2 text-sm text-gray-500">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Categories ──────────────────────────────────────────────────── */}
      <section className="bg-gray-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6">
          <h2 className="text-center text-3xl font-bold text-gray-900">
            Grants across every category
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-gray-500">
            We cover grants from SEAI, Revenue, DSP, Local Authorities, Enterprise Ireland, SUSI, HSE, and more.
          </p>

          <div className="mt-12 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {categories.map(([key, label]) => (
              <Link
                key={key}
                href={`/grants?category=${key}`}
                className="card flex flex-col items-center gap-2 py-8 text-center hover:border-brand-300"
              >
                <span className="text-3xl">{CATEGORY_ICONS[key] || '📋'}</span>
                <span className="text-sm font-semibold text-gray-700">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Example Result ──────────────────────────────────────────────── */}
      <section className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6">
          <div className="rounded-2xl bg-gradient-to-br from-brand-50 to-emerald-50 p-8 sm:p-12">
            <div className="text-center">
              <p className="text-sm font-semibold uppercase tracking-wider text-brand-600">Example result</p>
              <p className="mt-4 text-5xl font-extrabold text-brand-700 sm:text-6xl">€24,350</p>
              <p className="mt-2 text-lg text-gray-600">
                A Dublin homeowner with 2 children found 14 grants they qualify for
              </p>
            </div>
            <div className="mt-8 grid gap-3 sm:grid-cols-3">
              {[
                { cat: 'Home Energy', amount: '€12,200', count: '5 grants' },
                { cat: 'Tax Relief', amount: '€6,350', count: '4 grants' },
                { cat: 'Family', amount: '€5,800', count: '5 grants' },
              ].map((item) => (
                <div key={item.cat} className="rounded-lg bg-white/70 p-4 text-center">
                  <p className="text-sm font-medium text-gray-500">{item.cat}</p>
                  <p className="mt-1 text-xl font-bold text-gray-900">{item.amount}</p>
                  <p className="text-xs text-gray-400">{item.count}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ─── FAQ ─────────────────────────────────────────────────────────── */}
      <section className="bg-gray-50 py-16 sm:py-24">
        <div className="mx-auto max-w-3xl px-4 sm:px-6">
          <h2 className="text-center text-3xl font-bold text-gray-900">Frequently asked questions</h2>
          <div className="mt-10 space-y-6">
            {[
              { q: 'Is this really free?', a: 'Yes, the basic scan is completely free. You can see all the grants you qualify for and their match status. Full details, application guides, and PDF reports are available with a paid plan starting at €4.99.' },
              { q: 'How do you know which grants I qualify for?', a: 'Our rules engine contains eligibility criteria for 80+ Irish grants, schemes, and reliefs. We match your answers against these rules to determine eligibility. We update our database regularly to keep information current.' },
              { q: 'Is my data safe?', a: 'Absolutely. We take privacy seriously and comply with GDPR. Your answers are encrypted and never shared. You can delete your data at any time. We are not affiliated with any government body.' },
              { q: 'How accurate are the results?', a: 'Our matching is based on publicly available eligibility criteria. We classify matches as "Eligible" (strong match), "Likely" (most criteria met), or "Possible" (some criteria met). We always recommend verifying directly with the relevant organisation.' },
              { q: 'Do you apply for grants on my behalf?', a: 'No, we help you discover what you qualify for and provide step-by-step application guides. You apply directly to the relevant body (SEAI, Revenue, DSP, etc.).' },
            ].map((item) => (
              <details key={item.q} className="group rounded-lg bg-white p-6 shadow-sm">
                <summary className="flex cursor-pointer items-center justify-between font-semibold text-gray-900">
                  {item.q}
                  <span className="ml-4 text-brand-500 transition group-open:rotate-180">
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </span>
                </summary>
                <p className="mt-4 text-sm text-gray-500 leading-relaxed">{item.a}</p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Final CTA ───────────────────────────────────────────────────── */}
      <section className="bg-brand-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-4 text-center sm:px-6">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Don&apos;t leave money on the table
          </h2>
          <p className="mt-4 text-lg text-brand-100">
            Most Irish residents qualify for thousands in grants and entitlements they don&apos;t even know about. Find yours in under 3 minutes.
          </p>
          <Link href="/scan" className="mt-8 inline-block rounded-xl bg-white px-10 py-4 text-lg font-bold text-brand-700 shadow-lg transition hover:bg-brand-50 hover:shadow-xl">
            Start Your Free Scan
          </Link>
        </div>
      </section>
    </>
  );
}
