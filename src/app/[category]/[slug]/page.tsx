import { Metadata } from 'next'
import Script from 'next/script'
import { notFound } from 'next/navigation'
import { getPageByCategoryAndSlug, getAllPagePaths } from '@/lib/data-loader'

// Force Node.js runtime for fs access
export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
export const dynamicParams = true

interface PageProps {
  params: Promise<{
    category: string
    slug: string
  }>
}

export async function generateStaticParams() {
  const paths = getAllPagePaths()
  return paths.map(({ category, slug }) => ({
    category,
    slug,
  }))
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { category, slug } = await params
  const page = getPageByCategoryAndSlug(category, slug)

  if (!page) {
    return {
      title: 'Page Not Found',
    }
  }

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
    },
    twitter: {
      card: 'summary_large_image',
      title: page.title,
      description: page.description,
    },
    alternates: {
      canonical: `/${category}/${slug}`,
    },
  }
}

export default async function ContentPage({ params }: PageProps) {
  const { category, slug } = await params
  const page = getPageByCategoryAndSlug(category, slug)

  if (!page) {
    notFound()
  }

  // Generate Article Schema JSON-LD
  const siteUrl = process.env.SITE_URL || 'https://example.com'
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: page.title,
    description: page.description,
    url: `${siteUrl}/${category}/${slug}`,
    datePublished: page.published_at,
    dateModified: page.published_at,
    author: {
      '@type': 'Person',
      name: page.author || 'SEO Content Team',
    },
    publisher: {
      '@type': 'Organization',
      name: 'SEO Content Hub',
      url: siteUrl,
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${siteUrl}/${category}/${slug}`,
    },
    keywords: page.seo_keywords?.join(', ') || '',
    articleSection: category,
    wordCount: page.content?.split(/\s+/).length || 0,
  }

  // Parse content into sections (simple markdown-like parsing)
  const sections = page.content.split('\n\n').filter(Boolean)

  return (
    <>
      {/* JSON-LD Structured Data */}
      <Script
        id="article-schema"
        type="application/ld+json"
        strategy="beforeInteractive"
      >
        {JSON.stringify(articleSchema)}
      </Script>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Header */}
      <header className="mb-8">
        <div className="mb-4">
          <span className="text-sm font-medium text-blue-600 uppercase tracking-wide">
            {category}
          </span>
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          {page.title}
        </h1>
        <p className="text-xl text-gray-600 mb-4">
          {page.description}
        </p>

        {/* Meta info */}
        <div className="flex flex-wrap gap-4 text-sm text-gray-500">
          {page.published_at && (
            <span>Published: {page.published_at}</span>
          )}
          {page.author && (
            <span>By: {page.author}</span>
          )}
        </div>

        {/* Keywords */}
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

      {/* Content */}
      <article className="prose prose-gray max-w-none">
        {sections.map((section, index) => {
          // Check if it's a heading
          if (section.startsWith('## ')) {
            return (
              <h2
                key={index}
                className="text-2xl font-semibold text-gray-800 mt-8 mb-4"
              >
                {section.replace('## ', '')}
              </h2>
            )
          }
          if (section.startsWith('# ')) {
            return (
              <h1
                key={index}
                className="text-3xl font-bold text-gray-900 mt-8 mb-4"
              >
                {section.replace('# ', '')}
              </h1>
            )
          }

          // Check for list items
          if (section.includes('\n- ') || section.includes('\n1. ')) {
            const lines = section.split('\n')
            const isNumbered = lines.some((l) => /^\d+\./.test(l))

            return isNumbered ? (
              <ol key={index} className="list-decimal pl-6 my-4 space-y-2">
                {lines
                  .filter((l) => /^\d+\./.test(l))
                  .map((line, i) => (
                    <li key={i} className="text-gray-700">
                      {line.replace(/^\d+\.\s*/, '')}
                    </li>
                  ))}
              </ol>
            ) : (
              <ul key={index} className="list-disc pl-6 my-4 space-y-2">
                {lines
                  .filter((l) => l.startsWith('- '))
                  .map((line, i) => (
                    <li key={i} className="text-gray-700">
                      {line.replace('- ', '')}
                    </li>
                  ))}
              </ul>
            )
          }

          // Regular paragraph
          return (
            <p key={index} className="text-gray-700 mb-4 leading-relaxed">
              {section}
            </p>
          )
        })}
      </article>
    </div>
    </>
  )
}