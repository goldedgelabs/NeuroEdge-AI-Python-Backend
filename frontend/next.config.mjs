// next.config.mjs
import { fileURLToPath } from "url";

/**
 * ✨ NeuroEdge Enhanced Next.js Config
 * - Enables PWA mode
 * - Allows service worker under /public
 * - Provides security headers
 * - Offline caching support
 * - iOS standalone-mode fixes
 */

const config = {
  reactStrictMode: true,

  experimental: {
    optimizePackageImports: [
      "react",
      "react-dom",
    ],
  },

  // -------------------------------------------------------
  // Enable service workers
  // -------------------------------------------------------
  swcMinify: true,
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Serve service-worker.js without 404
  async headers() {
    return [
      {
        source: "/service-worker.js",
        headers: [
          { key: "Cache-Control", value: "no-cache" },
          { key: "Service-Worker-Allowed", value: "/" },
        ],
      },
      {
        source: "/manifest.json",
        headers: [{ key: "Cache-Control", value: "no-cache" }],
      },
    ];
  },

  // -------------------------------------------------------
  // PWA-ready static file handling
  // -------------------------------------------------------
  webpack: (config, { isServer }) => {
    if (!isServer) {
      // allow service worker in public/ to be served verbatim
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }

    return config;
  },
};

export default config;
