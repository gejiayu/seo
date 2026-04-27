import { Metadata } from 'next'
import Link from 'next/link'
import { getAllPages, getAllCategories } from '@/lib/data-loader'

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: 'SEO Content Hub',
    description: 'Browse all SEO-optimized content pages',
  }
}

export default function HomePage() {
  const pages = getAllPages()
  const categories = getAllCategories()

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          SEO Content Hub
        </h1>
        <p className="text-gray-600">
          Browse our collection of SEO-optimized content pages
        </p>
      </header>

      {/* Categories Overview */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Categories ({categories.length})
        </h2>
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <span
              key={category}
              className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
            >
              {category}
            </span>
          ))}
        </div>
      </section>

      {/* All Pages Listing */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          All Pages ({pages.length})
        </h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {pages.map(({ category, slug, data }) => (
            <Link
              key={`${category}/${slug}`}
              href={`/${category}/${slug}`}
              className="block p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
            >
              <div className="mb-2">
                <span className="text-xs font-medium text-blue-600 uppercase tracking-wide">
                  {category}
                </span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                {data.title}
              </h3>
              <p className="text-gray-600 text-sm line-clamp-3">
                {data.description}
              </p>
              {data.seo_keywords && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {data.seo_keywords.slice(0, 3).map((keyword) => (
                    <span
                      key={keyword}
                      className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              )}
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}