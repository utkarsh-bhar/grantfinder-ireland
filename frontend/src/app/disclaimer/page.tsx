import Link from 'next/link';

export const metadata = {
  title: 'Disclaimer — GrantFinder Ireland',
  description: 'Important disclaimer for GrantFinder Ireland. Information accuracy, eligibility, and professional advice.',
};

export default function DisclaimerPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 sm:py-16">
      <Link href="/" className="text-sm text-gray-500 hover:text-brand-600 transition-colors mb-6 inline-block">
        ← Back to GrantFinder
      </Link>

      <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">Disclaimer</h1>
      <p className="mt-2 text-sm text-gray-500">Last updated: February 2026</p>

      <div className="mt-10 space-y-10 text-gray-700 leading-relaxed">
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Information Accuracy</h2>
          <p>
            GrantFinder Ireland strives to provide accurate and up-to-date information about grants, schemes, reliefs,
            and entitlements in Ireland. However, grant programmes, eligibility criteria, amounts, and deadlines change
            frequently. We cannot guarantee the accuracy, completeness, or timeliness of the information on our platform.
            Information is compiled from publicly available sources and may not reflect the latest updates from grant
            providers or government bodies. We recommend that you always verify details directly with the relevant
            organisation before making any decisions or submitting applications.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Not Professional Advice</h2>
          <p>
            The content provided by GrantFinder Ireland is for general information and guidance purposes only. It does
            not constitute financial advice, legal advice, tax advice, or any other form of professional advice. We are
            not regulated as financial advisors, solicitors, or accountants. If you need professional advice tailored to
            your specific situation, you should consult a qualified advisor, such as a financial planner, solicitor, or
            tax professional, before relying on our information to make decisions.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Eligibility Is Indicative Only</h2>
          <p>
            Our eligibility matching results (e.g., &quot;Eligible&quot;, &quot;Likely&quot;, &quot;Possible&quot;) are
            based on the information you provide and our interpretation of publicly available eligibility criteria. They
            are indicative only and do not constitute a formal determination of your eligibility for any grant or
            scheme. Final eligibility is determined solely by the grant provider or administering body. Many grants
            involve subjective assessment, means-testing, or discretionary decisions that our automated system cannot
            replicate. You should never assume you are eligible for a grant based solely on our results—always confirm
            with the official source before applying.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Verify With Official Sources</h2>
          <p>
            GrantFinder Ireland encourages all users to verify grant information directly with the relevant organisation
            before applying. This includes checking official websites (e.g., SEAI, Revenue, Citizens Information, local
            authorities) for current eligibility criteria, amounts, application procedures, and closing dates. Links to
            external sources on our platform are provided for convenience; we do not control the content of external
            sites and are not responsible for their accuracy or availability.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">No Government Affiliation</h2>
          <p>
            GrantFinder Ireland is an independent service and is not affiliated with, endorsed by, or operated by any
            Irish government department, agency, or public body. We are not the Department of Social Protection, Revenue
            Commissioners, Sustainable Energy Authority of Ireland (SEAI), local authorities, or any other grant
            administrator. We simply compile and present information about grants to help users discover potential
            opportunities. Any references to government bodies or programmes are for informational purposes only.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">No Warranty</h2>
          <p>
            GrantFinder Ireland is provided &quot;as is&quot; without warranty of any kind. We disclaim all warranties,
            express or implied, including but not limited to warranties of accuracy, fitness for a particular purpose,
            or non-infringement. Use of our service is at your own risk.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Contact</h2>
          <p>
            For questions about this disclaimer, please contact us at{' '}
            <a href="mailto:privacy@grantfinder.ie" className="text-brand-600 hover:underline font-medium">
              privacy@grantfinder.ie
            </a>
            .
          </p>
        </section>
      </div>

      <div className="mt-12 pt-8 border-t border-gray-200">
        <Link href="/" className="text-brand-600 hover:text-brand-700 font-medium">
          Return to GrantFinder Ireland
        </Link>
      </div>
    </div>
  );
}
