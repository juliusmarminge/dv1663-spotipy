/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true,
  },
  redirects: async () => [
    { source: "/", destination: "/playlist/1", permanent: true },
    { source: "/playlist", destination: "/playlist/1", permanent: true },
  ],
  images: {
    remotePatterns: [{ protocol: "https", hostname: "i.pravatar.cc" }],
  },
};

module.exports = nextConfig;
