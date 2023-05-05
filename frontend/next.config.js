/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true,
  },
  redirects: async () => [
    { source: "/", destination: "/playlist/toplist", permanent: true },
  ],
};

module.exports = nextConfig;
