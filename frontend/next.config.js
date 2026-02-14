/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    // In production, proxy /api/* to the Fly.io backend
    // In local dev (when NEXT_PUBLIC_API_URL is not set), proxy to localhost
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'https://grantfinder-api.fly.dev';
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
