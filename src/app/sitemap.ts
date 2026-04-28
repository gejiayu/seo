import { MetadataRoute } from 'next'
import { getAllPages } from '@/lib/data-loader'

export default function sitemap(): MetadataRoute.Sitemap {
  const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'
  const pages = getAllPages()

  const postUrls = pages.map(({ slug, data }) => ({
    url: `${siteUrl}/posts/${slug}`,
    lastModified: data.published_at ? new Date(data.published_at) : new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }))

  return [
    {
      url: siteUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...postUrls,
  ]
}