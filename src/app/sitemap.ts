import { MetadataRoute } from 'next'
import { getAllPages } from '@/lib/data-loader'

export default function sitemap(): MetadataRoute.Sitemap {
  const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

  // English pages
  const enPages = getAllPages('en-US')
  const enUrls = enPages.map(({ slug, data }) => ({
    url: `${siteUrl}/posts/${slug}`,
    lastModified: data.published_at ? new Date(data.published_at) : new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }))

  // Chinese pages
  const zhPages = getAllPages('zh-CN')
  const zhUrls = zhPages.map(({ slug, data }) => ({
    url: `${siteUrl}/zh/posts/${slug}`,
    lastModified: data.published_at ? new Date(data.published_at) : new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }))

  return [
    // English homepage and legal pages
    { url: siteUrl, lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
    { url: `${siteUrl}/about-us`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
    { url: `${siteUrl}/privacy-policy`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.5 },
    { url: `${siteUrl}/terms-of-service`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.5 },
    // Chinese homepage and legal pages
    { url: `${siteUrl}/zh`, lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
    { url: `${siteUrl}/zh/about-us`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
    { url: `${siteUrl}/zh/privacy-policy`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.5 },
    { url: `${siteUrl}/zh/terms-of-service`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.5 },
    // All articles
    ...enUrls,
    ...zhUrls,
  ]
}
