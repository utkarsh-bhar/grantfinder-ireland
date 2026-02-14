import type { Metadata } from 'next';
import './globals.css';
import Header from '@/components/common/Header';
import Footer from '@/components/common/Footer';

export const metadata: Metadata = {
  title: 'GrantFinder Ireland — Discover Every Grant You Qualify For',
  description:
    'Answer a few questions and find every government grant, scheme, relief and entitlement you qualify for in Ireland. Housing, energy, business, welfare, education and more.',
  keywords:
    'Irish grants, SEAI grants, government grants Ireland, home energy grants, Help to Buy, welfare payments Ireland, business grants Ireland',
  openGraph: {
    title: 'GrantFinder Ireland',
    description: 'Discover every grant you qualify for in Ireland',
    url: 'https://grantfinder.ie',
    siteName: 'GrantFinder Ireland',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 flex flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
