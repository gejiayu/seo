import { Metadata } from 'next'
import Link from 'next/link'
import { getAllPages, getAllCategories } from '@/lib/data-loader'

export const runtime = 'nodejs'

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: 'HouseCar - Remote Work Tools & Productivity Guides',
    description: 'Discover the best remote work tools, productivity guides, and collaboration platforms for modern teams.',
  }
}

export default function HomePage() {
  const pages = getAllPages()
  const categories = getAllCategories()

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          HouseCar
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Discover the best remote work tools, productivity guides, and collaboration platforms for modern teams.
        </p>
      </header>

      {/* Categories Overview */}
      <section className="mb-10">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Categories ({categories.length})
        </h2>
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <span
              key={category}
              className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium capitalize"
            >
              {category}
            </span>
          ))}
        </div>
      </section>

      {/* All Pages Listing */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">
          All Articles ({pages.length})
        </h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {pages.map(({ slug, data }) => (
            <Link
              key={slug}
              href={`/posts/${slug}`}
              className="block p-6 bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-200 border border-gray-100 hover:border-blue-200"
            >
              <div className="mb-3">
                <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">
                  {data.category}
                </span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3 line-clamp-2 hover:text-blue-600 transition-colors">
                {data.title}
              </h3>
              <p className="text-gray-600 text-sm line-clamp-3 mb-4">
                {data.description}
              </p>
              {data.seo_keywords && data.seo_keywords.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {data.seo_keywords.slice(0, 3).map((keyword) => (
                    <span
                      key={keyword}
                      className="px-2 py-1 bg-gray-50 text-gray-500 text-xs rounded-md"
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