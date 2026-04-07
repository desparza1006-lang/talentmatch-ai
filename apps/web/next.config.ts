import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Environment variables exposed to the browser
  // MUST be set in Vercel Dashboard for production
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  // Note: rewrites removed - client calls API directly using NEXT_PUBLIC_API_URL
  // This requires CORS to be properly configured on the backend
};

export default nextConfig;
