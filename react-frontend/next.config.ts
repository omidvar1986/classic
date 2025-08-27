import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Remove serverActions as it's not supported in this Next.js version
  experimental: {
    optimizeCss: true,
  },
  // Handle font loading issues
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
        ],
      },
    ];
  },
  // Optimize images
  images: {
    domains: ['localhost', '127.0.0.1'],
    dangerouslyAllowSVG: true,
  },
};

export default nextConfig;
