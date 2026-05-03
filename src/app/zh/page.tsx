import { Metadata } from 'next'
import { getAllPagesList, getAllCategories } from '@/lib/data-loader'
import { ArticleList } from '@/components/ArticleList'

export const runtime = 'nodejs'

const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: 'HouseCar.life - 商业工具与软件对比指南 | 让业务自由驰骋',
    description: '覆盖120+行业的软件对比指南和商业工具评测。农业、汽车、医疗、建筑等行业最佳解决方案。选对工具，让业务自由驰骋。',
    alternates: {
      canonical: siteUrl,
      languages: {
        'en-US': siteUrl,
        'zh-CN': `${siteUrl}/zh`,
      },
    },
    openGraph: {
      title: 'HouseCar.life - 商业工具与软件对比指南',
      description: '覆盖120+行业的软件对比指南和商业工具评测。选对工具，让业务自由驰骋。',
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
        HouseCar.life - 商业工具与软件指南
      </h1>
      <p className="text-xl text-gray-600 max-w-2xl mx-auto">
        覆盖120+行业的软件对比指南和商业工具评测。农业、汽车、医疗、建筑等行业最佳解决方案。选对工具，让业务自由驰骋。
      </p>
      </header>

      <ArticleList pages={pages} categories={categories} language="zh-CN" />
    </div>
  )
}