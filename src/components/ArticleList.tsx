'use client'

import { useState } from 'react'
import Link from 'next/link'

interface PageData {
  title: string
  description: string
  content: string
  seo_keywords: string[]
  slug: string
  published_at?: string
  author?: string
  category: string
}

interface ArticleListProps {
  pages: Array<{ slug: string; data: PageData }>
  categories: string[]
}

export function ArticleList({ pages, categories }: ArticleListProps) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  const filteredPages = selectedCategory
    ? pages.filter((page) => page.data.category === selectedCategory)
    : pages

  return (
    <>
      {/* Categories Filter */}
      <section className="mb-10">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Categories ({categories.length})
        </h2>
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() =>
                setSelectedCategory(
                  selectedCategory === category ? null : category
                )
              }
              className={`px-4 py-2 rounded-full text-sm font-medium capitalize transition-all duration-200 cursor-pointer ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
              }`}
            >
              {category}
              {selectedCategory === category && (
                <span className="ml-2 opacity-80">✕</span>
              )}
            </button>
          ))}
        </div>
      </section>

      {/* All Pages Listing */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">
          {selectedCategory
            ? `${selectedCategory} Articles (${filteredPages.length})`
            : `All Articles (${pages.length})`}
        </h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredPages.map(({ slug, data }) => (
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

        {filteredPages.length === 0 && selectedCategory && (
          <div className="text-center py-12">
            <p className="text-gray-500">
              No articles found in this category.
            </p>
          </div>
        )}
      </section>
    </>
  )
}