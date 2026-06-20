import type { NextConfig } from "next";

const flaskApiUrl = process.env.FLASK_API_URL ?? "http://127.0.0.1:5000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/backend/:path*",
        destination: `${flaskApiUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
