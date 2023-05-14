/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true,
  },
  redirects: async () => [
    { source: "/", destination: "/playlist/toplist", permanent: true },
  ],
  images: {
    remotePatterns: [{ protocol: "https", hostname: "i.pravatar.cc" }],
  },
};

module.exports = nextConfig;
