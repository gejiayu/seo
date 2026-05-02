'use client'

import { useState, useMemo, useEffect } from 'react'
import Link from 'next/link'
import type { PageListItem, Language } from '@/lib/data-loader'
import { getCategoryName } from '@/lib/category-translations'

interface ArticleListProps {
  pages: PageListItem[]
  categories: string[]
  language?: Language
}

// 单个卡片组件
function ArticleCard({ page, language }: { page: PageListItem; language: Language }) {
  const href = language === 'zh-CN' ? `/zh/posts/${page.slug}` : `/posts/${page.slug}`

  return (
    <Link
      href={href}
      className="block p-6 bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-200 border border-gray-100 hover:border-blue-200"
    >
      <div className="mb-3">
        <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">
          {getCategoryName(page.category, language)}
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
  )
}

export function ArticleList({ pages, categories, language = 'en-US' }: ArticleListProps) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [showAllCategories, setShowAllCategories] = useState(false)
  const [visibleCount, setVisibleCount] = useState(50) // 首屏显示50篇
  const [isLoading, setIsLoading] = useState(false)

  // 默认显示前20个分类
  const visibleCategories = showAllCategories ? categories : categories.slice(0, 20)

  // 使用 useMemo 优化筛选性能
  const filteredPages = useMemo(() => {
    return selectedCategory
      ? pages.filter((page) => page.category === selectedCategory)
      : pages
  }, [pages, selectedCategory])

  // 当前显示的文章
  const displayedPages = filteredPages.slice(0, visibleCount)
  const hasMore = visibleCount < filteredPages.length

  // 加载更多
  const loadMore = () => {
    if (isLoading || !hasMore) return
    setIsLoading(true)
    // 模拟异步加载（实际是同步，但给用户视觉反馈）
    setTimeout(() => {
      setVisibleCount(prev => Math.min(prev + 50, filteredPages.length))
      setIsLoading(false)
    }, 100)
  }

  // 重置显示数量当筛选改变
  useEffect(() => {
    setVisibleCount(50)
  }, [selectedCategory])

  // 文本基于语言
  const texts = language === 'zh-CN'
    ? {
        categories: '分类',
        articles: '文章',
        allArticles: '全部文章',
        showAll: '显示全部',
        showLess: '显示较少',
        more: '更多',
        loadMore: '加载更多',
        remaining: '剩余',
        loading: '加载中...',
        noArticles: '该分类暂无文章',
      }
    : {
        categories: 'Categories',
        articles: 'Articles',
        allArticles: 'All Articles',
        showAll: 'Show All',
        showLess: 'Show Less',
        more: 'more',
        loadMore: 'Load More',
        remaining: 'remaining',
        loading: 'Loading...',
        noArticles: 'No articles found in this category',
      }

  return (
    <>
      {/* Categories Filter */}
      <section className="mb-10">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          {texts.categories} ({categories.length})
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
              {getCategoryName(category, language)}
              {selectedCategory === category && (
                <span className="ml-2 opacity-80">x</span>
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
            {showAllCategories ? texts.showLess : `${texts.showAll} (${categories.length - 20} ${texts.more})`}
          </button>
        )}
      </section>

      {/* All Pages Listing */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">
          {selectedCategory
            ? `${getCategoryName(selectedCategory, language)} ${texts.articles} (${filteredPages.length})`
            : `${texts.allArticles} (${pages.length})`}
        </h2>

        {displayedPages.length > 0 ? (
          <>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {displayedPages.map((page) => (
                <ArticleCard key={page.slug} page={page} language={language} />
              ))}
            </div>

            {/* Load More Button */}
            {hasMore && (
              <div className="mt-8 text-center">
                <button
                  onClick={loadMore}
                  disabled={isLoading}
                  className="px-6 py-3 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                >
                  {isLoading ? texts.loading : `${texts.loadMore} (${filteredPages.length - visibleCount} ${texts.remaining})`}
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">
              {texts.noArticles}
            </p>
          </div>
        )}
      </section>
    </>
  )
}