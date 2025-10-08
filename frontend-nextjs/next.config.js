/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  images: {
    domains: ['pcktfzshbxaljkbedrar.supabase.co', 'localhost'],
  },
}

module.exports = nextConfig

