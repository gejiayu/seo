'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname, useSearchParams } from 'next/navigation'
import type { PageListItem, Language } from '@/lib/data-loader'
import { getCategoryName } from '@/lib/category-translations'

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

interface HomePageClientProps {
  language?: Language
  initialCategory?: string
}

export default function HomePageClient({ language = 'en-US', initialCategory }: HomePageClientProps) {
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const [pages, setPages] = useState<PageListItem[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [total, setTotal] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(initialCategory || null)
  const [showAllCategories, setShowAllCategories] = useState(initialCategory ? true : false)
  const [page, setPage] = useState(1)

  // 初始加载
  useEffect(() => {
    const initLoad = async () => {
      setIsLoading(true)
      const params = new URLSearchParams({
        limit: selectedCategory ? '100' : '50',
        language,
      })
      if (selectedCategory) {
        params.set('category', selectedCategory)
      }

      const res = await fetch(`/api/pages?${params}`)
      const data = await res.json()
      setPages(data.pages)
      setCategories(data.categories || [])
      setTotal(data.total)
      setIsLoading(false)
    }

    initLoad()
  }, [language, selectedCategory])

  // 如果选中的类目不在前20个中，自动展开类目列表
  useEffect(() => {
    if (selectedCategory && categories.length > 20) {
      const isInFirst20 = categories.slice(0, 20).includes(selectedCategory)
      if (!isInFirst20) {
        setShowAllCategories(true)
      }
    }
  }, [selectedCategory, categories])

  const visibleCategories = showAllCategories ? categories : categories.slice(0, 20)
  const hasMore = pages.length < total

  // 加载更多
  const loadMore = async () => {
    if (isLoading || !hasMore) return
    setIsLoading(true)

    try {
      const nextPage = page + 1
      const params = new URLSearchParams({
        page: nextPage.toString(),
        limit: '50',
        language,
      })
      if (selectedCategory) {
        params.set('category', selectedCategory)
      }

      const res = await fetch(`/api/pages?${params}`)
      const data = await res.json()

      setPages(prev => [...prev, ...data.pages])
      setPage(nextPage)
    } catch (error) {
      console.error('Failed to load more pages:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // 分类筛选
  const handleCategorySelect = async (category: string | null) => {
    const newCategory = selectedCategory === category ? null : category
    setSelectedCategory(newCategory)
    setIsLoading(true)
    setPage(1)

    // 更新 URL 参数
    if (newCategory) {
      window.history.pushState(null, '', `${pathname}?category=${newCategory}`)
    } else {
      window.history.pushState(null, '', pathname)
    }

    if (!newCategory) {
      // 重置为初始数据
      const res = await fetch(`/api/pages?limit=50&language=${language}`)
      const data = await res.json()
      setPages(data.pages)
      setTotal(data.total)
      setIsLoading(false)
      return
    }

    const res = await fetch(`/api/pages?category=${newCategory}&limit=100&language=${language}`)
    const data = await res.json()
    setPages(data.pages)
    setTotal(data.total)
    setIsLoading(false)
  }

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
        subtitle: '🚀 用对工具，自由工作，自由生活',
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
        subtitle: '🚀 Free Your Business with the Right Tools — Work Anywhere, Live Freely',
      }

  if (isLoading && pages.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-500">{texts.loading}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          HouseCar.life - Business Tools & Software Guides
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Comprehensive software comparison guides and business tools reviews for 120+ industries.
        </p>
        <p className="text-lg text-blue-600 mt-4 font-medium">
          {texts.subtitle}
        </p>
      </header>

      {/* Categories Filter */}
      <section className="mb-10">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          {texts.categories} ({categories.length})
        </h2>
        <div className="flex flex-wrap gap-2 mb-4">
          {visibleCategories.map((category) => (
            <button
              key={category}
              onClick={() => handleCategorySelect(category)}
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

        {categories.length > 20 && (
          <button
            onClick={() => setShowAllCategories(!showAllCategories)}
            className="px-4 py-2 rounded-full text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-all duration-200 cursor-pointer"
          >
            {showAllCategories ? texts.showLess : `${texts.showAll} (${categories.length - 20} ${texts.more})`}
          </button>
        )}
      </section>

      {/* Articles */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">
          {selectedCategory
            ? `${getCategoryName(selectedCategory, language)} ${texts.articles} (${total})`
            : `${texts.allArticles} (${total})`}
        </h2>

        {pages.length > 0 ? (
          <>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {pages.map((pageItem) => (
                <ArticleCard key={pageItem.slug} page={pageItem} language={language} />
              ))}
            </div>

            {hasMore && (
              <div className="mt-8 text-center">
                <button
                  onClick={loadMore}
                  disabled={isLoading}
                  className="px-6 py-3 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                >
                  {isLoading ? texts.loading : `${texts.loadMore} (${total - pages.length} ${texts.remaining})`}
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">{texts.noArticles}</p>
          </div>
        )}
      </section>
    </div>
  )
}