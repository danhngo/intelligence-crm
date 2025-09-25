/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    appDir: true,
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
    NEXT_PUBLIC_CRM_API_URL: process.env.NEXT_PUBLIC_CRM_API_URL || 'http://localhost:8001',
    NEXT_PUBLIC_USER_API_URL: process.env.NEXT_PUBLIC_USER_API_URL || 'http://localhost:8002',
    NEXT_PUBLIC_WORKFLOW_API_URL: process.env.NEXT_PUBLIC_WORKFLOW_API_URL || 'http://localhost:8003',
    NEXT_PUBLIC_AI_API_URL: process.env.NEXT_PUBLIC_AI_API_URL || 'http://localhost:8004',
  }
}

module.exports = nextConfig
