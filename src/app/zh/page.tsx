import { Metadata } from 'next'
import HomePageClient from '@/components/HomePageClient'

export const runtime = 'nodejs'

const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: 'HouseCar.life - 商业工具与软件对比指南 | 让业务自由驰骋',
    description: '覆盖120+行业的软件对比指南和商业工具评测。农业、汽车、医疗、建筑等行业最佳解决方案。选对工具，让业务自由驰骋。',
    alternates: {
      canonical: `${siteUrl}/zh`,
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

interface ZhHomePageProps {
  searchParams: Promise<{
    category?: string
  }>
}

export default async function ZhHomePage({ searchParams }: ZhHomePageProps) {
  const { category } = await searchParams
  return <HomePageClient language="zh-CN" initialCategory={category} />
}