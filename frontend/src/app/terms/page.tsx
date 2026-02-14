import Link from 'next/link';

export const metadata = {
  title: 'Terms of Service — GrantFinder Ireland',
  description: 'Terms of service for GrantFinder Ireland. Read our service description, disclaimers, and user responsibilities.',
};

export default function TermsPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 sm:py-16">
      <Link href="/" className="text-sm text-gray-500 hover:text-brand-600 transition-colors mb-6 inline-block">
        ← Back to GrantFinder
      </Link>

      <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">Terms of Service</h1>
      <p className="mt-2 text-sm text-gray-500">Last updated: February 2026</p>

      <div className="mt-10 space-y-10 text-gray-700 leading-relaxed">
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">1. Service Description</h2>
          <p>
            GrantFinder Ireland provides an online grant eligibility scanning service. Users answer a series of
            questions about their circumstances, and we use this information to suggest grants, schemes, reliefs, and
            entitlements that may be relevant to them. Our service is informational in nature and is designed to help
            users discover potential funding opportunities in Ireland.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">2. Disclaimer — Informational Only</h2>
          <p>
            <strong>Our results are for informational purposes only and do not constitute professional advice.</strong>{' '}
            GrantFinder Ireland is not a licensed financial advisor, legal advisor, or government agency. The
            eligibility assessments, grant amounts, and recommendations provided through our service are indicative only
            and are based on publicly available information. We do not guarantee that you will qualify for any grant or
            that our information is complete, accurate, or up to date. Users should always verify eligibility criteria,
            amounts, and application requirements directly with the relevant official sources before applying.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">3. User Responsibilities</h2>
          <p className="mb-2">By using our service, you agree to:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>Provide accurate and truthful information when completing the questionnaire.</li>
            <li>Use the service only for lawful purposes and in accordance with these Terms.</li>
            <li>Verify any grant eligibility and application details with official sources before applying.</li>
            <li>Not misuse, reverse-engineer, or attempt to gain unauthorized access to our systems or data.</li>
            <li>Not use the service in any way that could harm, disable, or impair our platform or other users.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">4. Intellectual Property</h2>
          <p>
            All content, design, branding, and software on the GrantFinder Ireland platform are owned by or licensed to
            GrantFinder Ireland. This includes but is not limited to text, graphics, logos, and the structure of the
            questionnaire and results. You may not copy, modify, distribute, or create derivative works from our
            content without our prior written permission. Grant information is compiled from publicly available sources;
            the presentation, organisation, and matching logic are our intellectual property.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">5. Limitation of Liability</h2>
          <p>
            To the fullest extent permitted by law, GrantFinder Ireland shall not be liable for any indirect,
            incidental, special, consequential, or punitive damages arising from your use of our service. Our total
            liability for any claim arising from these Terms or your use of the service shall not exceed the amount you
            paid to us (if any) in the twelve months preceding the claim. We do not warrant that our service will be
            uninterrupted, error-free, or free of harmful components. You use our service at your own risk.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">6. Governing Law</h2>
          <p>
            These Terms of Service are governed by the laws of Ireland. Any disputes arising from or relating to these
            Terms or the use of our service shall be subject to the exclusive jurisdiction of the courts of Ireland.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">7. Changes to Terms</h2>
          <p>
            We reserve the right to modify these Terms at any time. Changes will be effective when posted on this page
            with an updated &quot;Last updated&quot; date. Your continued use of the service after changes constitutes
            acceptance of the revised Terms. If you do not agree to the new Terms, you must stop using our service.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">8. Contact</h2>
          <p>
            For questions about these Terms of Service, please contact us at{' '}
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
