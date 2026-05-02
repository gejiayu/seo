import { Metadata } from 'next'
import Script from 'next/script'
import fs from 'fs'
import path from 'path'

export const runtime = 'nodejs'

interface PageData {
  title: string
  description: string
  content: string
  seo_keywords?: string[]
  published_at?: string
  author?: string
}

function getAboutUsData(): PageData | null {
  try {
    const filePath = path.join(process.cwd(), 'data/legal/about-us.json')
    const content = fs.readFileSync(filePath, 'utf8')
    return JSON.parse(content)
  } catch (error) {
    return null
  }
}

const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

export async function generateMetadata(): Promise<Metadata> {
  const data = getAboutUsData()

  if (!data) {
    return { title: 'About Us' }
  }

  return {
    title: data.title,
    description: data.description,
    keywords: data.seo_keywords,
    alternates: {
      canonical: `${siteUrl}/about-us`, // 绝对URL
    },
    openGraph: {
      title: data.title,
      description: data.description,
      type: 'article',
      url: `${siteUrl}/about-us`,
    },
    twitter: {
      card: 'summary_large_image',
      title: data.title,
      description: data.description,
    },
  }
}

export default function AboutUsPage() {
  const data = getAboutUsData()
  const currentSiteUrl = process.env.SITE_URL || 'https://www.housecar.life'

  if (!data) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">About Us</h1>
        <p className="text-gray-600">About us content is being updated.</p>
      </div>
    )
  }

  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: data.title,
    description: data.description,
    url: `${currentSiteUrl}/about-us`,
    datePublished: data.published_at,
    dateModified: data.published_at,
    author: {
      '@type': 'Organization',
      name: data.author || 'HouseCar Team',
    },
    publisher: {
      '@type': 'Organization',
      name: 'HouseCar',
      url: siteUrl,
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${siteUrl}/about-us`,
    },
  }

  return (
    <>
      <Script
        id="about-us-schema"
        type="application/ld+json"
        strategy="beforeInteractive"
      >
        {JSON.stringify(articleSchema)}
      </Script>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="mb-8">
          <div className="mb-4">
            <span className="text-sm font-medium text-blue-600 uppercase tracking-wide">
              About
            </span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            {data.title}
          </h1>
          <p className="text-xl text-gray-600 mb-4">
            {data.description}
          </p>

          <div className="flex flex-wrap gap-4 text-sm text-gray-500">
            {data.published_at && (
              <span>Published: {data.published_at}</span>
            )}
            {data.author && (
              <span>By: {data.author}</span>
            )}
          </div>

          {data.seo_keywords && (
            <div className="mt-4 flex flex-wrap gap-2">
              {data.seo_keywords.map((keyword) => (
                <span
                  key={keyword}
                  className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full"
                >
                  {keyword}
                </span>
              ))}
            </div>
          )}
        </header>

        <article className="prose prose-gray max-w-none">
          <div dangerouslySetInnerHTML={{ __html: data.content }} />
        </article>
      </div>
    </>
  )
}