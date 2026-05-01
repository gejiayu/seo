'use client'

import { useState, useMemo } from 'react'
import Link from 'next/link'
import type { PageListItem } from '@/lib/data-loader'

interface ArticleListProps {
  pages: PageListItem[]
  categories: string[]
}

export function ArticleList({ pages, categories }: ArticleListProps) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [showAllCategories, setShowAllCategories] = useState(false)

  // 默认显示前20个分类
  const visibleCategories = showAllCategories ? categories : categories.slice(0, 20)

  // 使用 useMemo 优化筛选性能
  const filteredPages = useMemo(() => {
    return selectedCategory
      ? pages.filter((page) => page.category === selectedCategory)
      : pages
  }, [pages, selectedCategory])

  return (
    <>
      {/* Categories Filter */}
      <section className="mb-10">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Categories ({categories.length})
        </h2>
        <div className="flex flex-wrap gap-2 mb-4">
          {visibleCategories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(
                  selectedCategory === category ? null : category
                )}
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

        {/* Show More/Less Button */}
        {categories.length > 20 && (
          <button
            onClick={() => setShowAllCategories(!showAllCategories)}
            className="px-4 py-2 rounded-full text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-all duration-200 cursor-pointer"
          >
            {showAllCategories ? 'Show Less' : `Show All (${categories.length - 20} more)`}
          </button>
        )}
      </section>

      {/* All Pages Listing */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">
          {selectedCategory
            ? `${selectedCategory} Articles (${filteredPages.length})`
            : `All Articles (${pages.length})`}
        </h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredPages.map((page) => (
            <Link
              key={page.slug}
              href={`/posts/${page.slug}`}
              className="block p-6 bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-200 border border-gray-100 hover:border-blue-200"
            >
              <div className="mb-3">
                <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">
                  {page.category}
                </span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3 line-clamp-2 hover:text-blue-600 transition-colors">
                {page.title}
              </h3>
              <p className="text-gray-600 text-sm line-clamp-3 mb-4">
                {page.description}
              </p>
              {page.seo_keywords && page.seo_keywords.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {page.seo_keywords.slice(0, 3).map((keyword) => (
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