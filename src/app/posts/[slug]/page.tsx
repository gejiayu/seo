import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { getAllPages, getAllPagePaths } from '@/lib/data-loader'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
export const dynamicParams = true

interface PageProps {
  params: Promise<{
    slug: string
  }>
}

function getPageBySlug(slug: string) {
  const pages = getAllPages()
  return pages.find((p) => p.slug === slug)?.data || null
}

export async function generateStaticParams() {
  const paths = getAllPagePaths()
  return paths.map(({ slug }) => ({ slug }))
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params
  const page = getPageBySlug(slug)

  if (!page) {
    return { title: 'Page Not Found' }
  }

  const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

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
      url: `${siteUrl}/posts/${slug}`,
    },
    twitter: {
      card: 'summary_large_image',
      title: page.title,
      description: page.description,
    },
    alternates: {
      canonical: `${siteUrl}/posts/${slug}`, // 绝对URL，明确告诉Google"正主"是谁
    },
  }
}

export default async function PostPage({ params }: PageProps) {
  const { slug } = await params
  const page = getPageBySlug(slug)

  if (!page) {
    notFound()
  }

  const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: page.title,
    description: page.description,
    url: `${siteUrl}/posts/${slug}`,
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
      '@id': `${siteUrl}/posts/${slug}`,
    },
    keywords: page.seo_keywords?.join(', ') || '',
    articleSection: page.category,
    wordCount: page.content?.split(/\s+/).length || 0,
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(articleSchema),
        }}
      />

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
              <span>Published: {page.published_at}</span>
            )}
            {page.author && (
              <span>By: {page.author}</span>
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