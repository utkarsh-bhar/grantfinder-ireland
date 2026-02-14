import Link from 'next/link';

export const metadata = {
  title: 'Privacy Policy — GrantFinder Ireland',
  description: 'GDPR-compliant privacy policy for GrantFinder Ireland. Learn how we collect, use, and protect your data.',
};

export default function PrivacyPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 sm:py-16">
      <Link href="/" className="text-sm text-gray-500 hover:text-brand-600 transition-colors mb-6 inline-block">
        ← Back to GrantFinder
      </Link>

      <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">Privacy Policy</h1>
      <p className="mt-2 text-sm text-gray-500">Last updated: February 2026</p>

      <div className="mt-10 space-y-10 text-gray-700 leading-relaxed">
        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">1. Introduction</h2>
          <p>
            GrantFinder Ireland (&quot;we&quot;, &quot;us&quot;, &quot;our&quot;) is committed to protecting your privacy. This Privacy Policy explains
            how we collect, use, store, and protect your personal data when you use our grant-finding service at
            grantfinder.ie, in compliance with the General Data Protection Regulation (GDPR) and Irish data protection law.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">2. Data Controller</h2>
          <p>
            The data controller responsible for your personal data is GrantFinder Ireland. For any data protection
            enquiries, please contact us at{' '}
            <a href="mailto:privacy@grantfinder.ie" className="text-brand-600 hover:underline font-medium">
              privacy@grantfinder.ie
            </a>
            .
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">3. What Data We Collect</h2>
          <p className="mb-2">We collect the following categories of personal data:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>
              <strong>Profile and questionnaire answers:</strong> Information you provide when completing our grant
              eligibility scan, including details about your home, family, employment, income, welfare status, and other
              relevant circumstances. This data is used solely to match you with relevant grants and schemes.
            </li>
            <li>
              <strong>Email address:</strong> If you choose to create an account or request a report, we collect your
              email address for communication purposes.
            </li>
            <li>
              <strong>Technical data:</strong> IP address, browser type, and device information may be collected
              automatically for security and service improvement purposes.
            </li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">4. How We Use Your Data</h2>
          <p>
            Your data is used exclusively for grant matching and improving our service. We use your profile answers to
            calculate which grants, schemes, and reliefs you may be eligible for. We do not use your data for marketing,
            advertising, or any purpose other than delivering the grant-finding service you have requested.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">5. How We Store Your Data</h2>
          <p>
            All personal data is stored securely using industry-standard encryption. Our servers and data processing
            facilities are located within the European Union (EU) to ensure compliance with GDPR and Irish data
            protection requirements. We retain your data only for as long as necessary to provide our services or as
            required by law.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">6. Third-Party Sharing</h2>
          <p>
            We do not sell, rent, or share your personal data with third parties for marketing or any other purpose.
            Your profile answers and contact details are never shared with grant providers, government agencies, or
            advertisers. We may share data only with trusted service providers (e.g., hosting, payment processing) who
            are bound by strict confidentiality and data protection obligations.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">7. Your Rights Under GDPR</h2>
          <p className="mb-3">You have the following rights regarding your personal data:</p>
          <ul className="list-disc pl-6 space-y-1">
            <li>
              <strong>Right of access:</strong> You may request a copy of the personal data we hold about you.
            </li>
            <li>
              <strong>Right to rectification:</strong> You may request that we correct any inaccurate or incomplete
              data.
            </li>
            <li>
              <strong>Right to erasure:</strong> You may request that we delete your personal data (subject to legal
              retention requirements).
            </li>
            <li>
              <strong>Right to data portability:</strong> You may request a copy of your data in a machine-readable
              format.
            </li>
            <li>
              <strong>Right to restrict processing:</strong> You may request that we limit how we use your data.
            </li>
            <li>
              <strong>Right to object:</strong> You may object to certain types of processing.
            </li>
            <li>
              <strong>Right to withdraw consent:</strong> Where processing is based on consent, you may withdraw it at
              any time.
            </li>
          </ul>
          <p className="mt-3">
            To exercise any of these rights, please contact us at{' '}
            <a href="mailto:privacy@grantfinder.ie" className="text-brand-600 hover:underline font-medium">
              privacy@grantfinder.ie
            </a>
            . You also have the right to lodge a complaint with the Data Protection Commission (Ireland) if you believe
            your rights have been violated.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">8. Cookies</h2>
          <p>
            We use only essential cookies that are necessary for the operation of our website. These include cookies
            for session management and security. We do not use advertising, tracking, or analytical cookies that
            collect personal data for third-party purposes. By using our site, you consent to the use of these essential
            cookies.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">9. Changes to This Policy</h2>
          <p>
            We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated
            &quot;Last updated&quot; date. We encourage you to review this policy periodically.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-900 mb-3">10. Contact</h2>
          <p>
            For any questions about this Privacy Policy or your personal data, please contact us at{' '}
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
