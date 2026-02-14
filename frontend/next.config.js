/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    // In production (Vercel), proxy /api/* to the Render backend
    // In local dev, proxy to localhost:8000
    const destination = apiUrl
      ? `${apiUrl}/:path*`
      : 'http://localhost:8000/api/:path*';
    return [
      {
        source: '/api/:path*',
        destination,
      },
    ];
  },
};

module.exports = nextConfig;
