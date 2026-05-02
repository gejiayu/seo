import { Metadata } from 'next'
import { getAllPagesList, getAllCategories } from '@/lib/data-loader'
import { ArticleList } from '@/components/ArticleList'

export const runtime = 'nodejs'

const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: 'HouseCar - 远程工作工具与生产力指南',
    description: '发现最佳远程工作工具、生产力指南和协作平台，助力现代团队高效协作。',
    alternates: {
      canonical: siteUrl, // 中文首页canonical指向英文首页（防止重复内容）
      languages: {
        'en-US': siteUrl,
        'zh-CN': `${siteUrl}/zh`,
      },
    },
    openGraph: {
      title: 'HouseCar - 远程工作工具与生产力指南',
      description: '发现最佳远程工作工具、生产力指南和协作平台，助力现代团队高效协作。',
      url: `${siteUrl}/zh`,
      type: 'website',
      siteName: 'HouseCar',
      locale: 'zh_CN',
    },
  }
}

export default function ZhHomePage() {
  const pages = getAllPagesList('zh-CN') // Chinese articles only
  const categories = getAllCategories('zh-CN') // Chinese categories only

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          HouseCar
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          发现最佳远程工作工具、生产力指南和协作平台，助力现代团队高效协作。
        </p>
      </header>

      <ArticleList pages={pages} categories={categories} language="zh-CN" />
    </div>
  )
}