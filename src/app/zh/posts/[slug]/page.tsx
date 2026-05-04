import { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getAllPages, getAllPagePaths, getPageBySlug, getPagesByCategory, type Language } from '@/lib/data-loader'
import { truncateDescription, generateOgImage, formatCategoryName } from '@/lib/seo-helpers'

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
  const metaDescription = truncateDescription(page.description, 155)
  const ogImage = generateOgImage(page.title, page.category)
  const canonicalUrl = page.canonical_link || `${siteUrl}/posts/${slug}`

  return {
    title: page.title,
    description: metaDescription,
    keywords: page.seo_keywords,
    openGraph: {
      title: page.title,
      description: metaDescription,
      type: 'article',
      publishedTime: page.published_at,
      authors: page.author ? [page.author] : undefined,
      url: `${siteUrl}/zh/posts/${slug}`,
      images: [
        {
          url: ogImage,
          width: 1200,
          height: 630,
          alt: page.title,
        },
      ],
      locale: 'zh_CN',
    },
    twitter: {
      card: 'summary_large_image',
      title: page.title,
      description: metaDescription,
      images: [ogImage],
    },
    alternates: {
      canonical: canonicalUrl,
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
  const ogImage = generateOgImage(page.title, page.category)
  const metaDescription = truncateDescription(page.description, 155)

  // Article Schema with image
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: page.title,
    description: metaDescription,
    image: [ogImage],
    url: `${siteUrl}/zh/posts/${slug}`,
    datePublished: page.published_at,
    dateModified: page.published_at,
    author: {
      '@type': 'Person',
      name: page.author || 'HouseCar Team',
      url: `${siteUrl}/zh/authors/${(page.author || 'housecar-team').toLowerCase().replace(/\s+/g, '-')}`,
    },
    publisher: {
      '@type': 'Organization',
      name: 'HouseCar',
      url: siteUrl,
      logo: {
        '@type': 'ImageObject',
        url: `${siteUrl}/logo.png`,
      },
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

  // Breadcrumb Schema
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: '首页',
        item: `${siteUrl}/zh`,
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: formatCategoryName(page.category),
        item: `${siteUrl}/zh/categories/${page.category}`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: page.title,
        item: `${siteUrl}/zh/posts/${slug}`,
      },
    ],
  }

  // Get related articles (same category, excluding current)
  const categoryPages = getPagesByCategory(page.category, 'zh-CN')
    .filter(p => p.slug !== slug)
    .slice(0, 6)

  return (
    <>
      {/* Article Schema - Static SSR for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
      />
      {/* Breadcrumb Schema - Static SSR for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />

      {/* Breadcrumb Navigation */}
      <nav className="container mx-auto px-4 py-2 max-w-4xl">
        <ol className="flex items-center gap-2 text-sm text-gray-600">
          <li>
            <Link href="/zh" className="hover:text-blue-600">
              首页
            </Link>
          </li>
          <li>/</li>
          <li>
            <Link
              href={`/zh?category=${page.category}`}
              className="hover:text-blue-600"
            >
              {formatCategoryName(page.category)}
            </Link>
          </li>
          <li>/</li>
          <li className="text-gray-900 truncate max-w-xs">
            {page.title}
          </li>
        </ol>
      </nav>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="mb-8">
          <div className="mb-4">
            <Link
              href={`/zh?category=${page.category}`}
              className="text-sm font-medium text-blue-600 uppercase tracking-wide hover:text-blue-800"
            >
              {formatCategoryName(page.category)}
            </Link>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            {page.title}
          </h1>
          <p className="text-xl text-gray-600 mb-4">
            {metaDescription}
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

        {/* Related Articles */}
        {categoryPages.length > 0 && (
          <section className="mt-12 pt-8 border-t border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              {formatCategoryName(page.category)} 相关文章
            </h2>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {categoryPages.map((related) => (
                <Link
                  key={related.slug}
                  href={`/zh/posts/${related.slug}`}
                  className="block p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                    {related.data.title}
                  </h3>
                  <p className="text-sm text-gray-600 line-clamp-3">
                    {truncateDescription(related.data.description, 100)}
                  </p>
                </Link>
              ))}
            </div>
          </section>
        )}
      </div>
    </>
  )
}