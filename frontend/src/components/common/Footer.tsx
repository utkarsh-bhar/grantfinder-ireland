import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <span className="text-xl">🍀</span>
              <span className="font-bold text-brand-700">GrantFinder.ie</span>
            </div>
            <p className="text-sm text-gray-500">
              Helping Irish residents discover every grant and entitlement they qualify for.
            </p>
          </div>

          <div>
            <h4 className="mb-3 text-sm font-semibold text-gray-900">Product</h4>
            <nav className="flex flex-col gap-2">
              <Link href="/scan" className="text-sm text-gray-500 hover:text-brand-600">Find Grants</Link>
              <Link href="/grants" className="text-sm text-gray-500 hover:text-brand-600">Browse All</Link>
              <Link href="/pricing" className="text-sm text-gray-500 hover:text-brand-600">Pricing</Link>
            </nav>
          </div>

          <div>
            <h4 className="mb-3 text-sm font-semibold text-gray-900">Categories</h4>
            <nav className="flex flex-col gap-2">
              <Link href="/grants?category=home_energy" className="text-sm text-gray-500 hover:text-brand-600">Home Energy</Link>
              <Link href="/grants?category=housing" className="text-sm text-gray-500 hover:text-brand-600">Housing</Link>
              <Link href="/grants?category=business" className="text-sm text-gray-500 hover:text-brand-600">Business</Link>
              <Link href="/grants?category=welfare" className="text-sm text-gray-500 hover:text-brand-600">Welfare</Link>
            </nav>
          </div>

          <div>
            <h4 className="mb-3 text-sm font-semibold text-gray-900">Legal</h4>
            <nav className="flex flex-col gap-2">
              <Link href="/privacy" className="text-sm text-gray-500 hover:text-brand-600">Privacy Policy</Link>
              <Link href="/terms" className="text-sm text-gray-500 hover:text-brand-600">Terms of Service</Link>
              <Link href="/disclaimer" className="text-sm text-gray-500 hover:text-brand-600">Disclaimer</Link>
            </nav>
          </div>
        </div>

        <div className="mt-8 border-t border-gray-100 pt-6 text-center text-xs text-gray-400">
          <p>&copy; {new Date().getFullYear()} GrantFinder Ireland. Not affiliated with any Irish government department or agency.</p>
          <p className="mt-1">Information is for guidance only. Verify eligibility with the relevant organisation before applying.</p>
        </div>
      </div>
    </footer>
  );
}
