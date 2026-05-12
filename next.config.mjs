/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: false, // 统一URL格式，避免Google因斜杠问题产生两次爬取
  output: 'export', // Static export for Cloudflare Pages direct upload
}

export default nextConfig