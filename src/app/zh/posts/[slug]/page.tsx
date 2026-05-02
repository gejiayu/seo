import { Metadata } from 'next'
import Script from 'next/script'
import { notFound } from 'next/navigation'
import { getAllPages, getAllPagePaths, getPageBySlug, type Language } from '@/lib/data-loader'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
export const dynamicParams = true

interface PageProps {
  params: Promise<{
    slug: string
  }>
}

export async function generateStaticParams() {
  const paths = getAllPagePaths('zh-CN')
  return paths.map(({ slug }) => ({ slug }))
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params
  const page = getPageBySlug(slug, 'zh-CN')

  if (!page) {
    return { title: '页面未找到' }
  }

  const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'
  const canonicalUrl = page.canonical_link || `${siteUrl}/posts/${slug}`

  return {
    title: page.title,
    description: page.description,
    keywords: page.seo_keywords,
    openGraph: {
      title: page.title,
      description: page.description,
      type: 'article',
      publishedTime: page.published_at,
      authors: page.author ? [page.author] : undefined,
      url: `${siteUrl}/zh/posts/${slug}`,
      locale: 'zh_CN',
    },
    twitter: {
      card: 'summary_large_image',
      title: page.title,
      description: page.description,
    },
    alternates: {
      canonical: canonicalUrl, // 中文页canonical指向英文URL
      languages: page.alternate_links || {
        'en-US': `${siteUrl}/posts/${slug}`,
        'zh-CN': `${siteUrl}/zh/posts/${slug}`,
      },
    },
  }
}

export default async function ZhPostPage({ params }: PageProps) {
  const { slug } = await params
  const page = getPageBySlug(slug, 'zh-CN')

  if (!page) {
    notFound()
  }

  const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: page.title,
    description: page.description,
    url: `${siteUrl}/zh/posts/${slug}`,
    datePublished: page.published_at,
    dateModified: page.published_at,
    author: {
      '@type': 'Person',
      name: page.author || 'HouseCar Team',
    },
    publisher: {
      '@type': 'Organization',
      name: 'HouseCar',
      url: siteUrl,
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${siteUrl}/zh/posts/${slug}`,
    },
    keywords: page.seo_keywords?.join(', ') || '',
    articleSection: page.category,
    wordCount: page.content?.split(/\s+/).length || 0,
    inLanguage: 'zh-CN',
  }

  return (
    <>
      <Script
        id="article-schema"
        type="application/ld+json"
        strategy="beforeInteractive"
      >
        {JSON.stringify(articleSchema)}
      </Script>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="mb-8">
          <div className="mb-4">
            <span className="text-sm font-medium text-blue-600 uppercase tracking-wide">
              {page.category}
            </span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            {page.title}
          </h1>
          <p className="text-xl text-gray-600 mb-4">
            {page.description}
          </p>

          <div className="flex flex-wrap gap-4 text-sm text-gray-500">
            {page.published_at && (
              <span>发布于: {page.published_at}</span>
            )}
            {page.author && (
              <span>作者: {page.author}</span>
            )}
          </div>

          {page.seo_keywords && (
            <div className="mt-4 flex flex-wrap gap-2">
              {page.seo_keywords.map((keyword) => (
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
          <div dangerouslySetInnerHTML={{ __html: page.content }} />
        </article>
      </div>
    </>
  )
}