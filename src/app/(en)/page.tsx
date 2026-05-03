import { Metadata } from 'next'
import { getAllPagesList, getAllCategories } from '@/lib/data-loader'
import { ArticleList } from '@/components/ArticleList'

export const runtime = 'nodejs'

const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: 'HouseCar.life - Business Tools & Software Comparison Guides | Free Your Business',
    description: 'Comprehensive software comparison guides and business tools reviews for 120+ industries. Find the best solutions for agriculture, automotive, healthcare, construction, and more. Free your business with the right tools.',
    alternates: {
      canonical: siteUrl,
      languages: {
        'en-US': siteUrl,
        'zh-CN': `${siteUrl}/zh`,
      },
    },
    openGraph: {
      title: 'HouseCar.life - Business Tools & Software Guides',
      description: 'Comprehensive software comparison guides and business tools reviews for 120+ industries. Free your business with the right tools.',
      url: siteUrl,
      type: 'website',
      siteName: 'HouseCar',
      locale: 'en_US',
    },
  }
}

export default function HomePage() {
  const pages = getAllPagesList('en-US') // Lightweight version without content field - English only
  const categories = getAllCategories('en-US') // English categories only

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
        HouseCar.life - Business Tools & Software Guides
      </h1>
      <p className="text-xl text-gray-600 max-w-2xl mx-auto">
        Comprehensive software comparison guides and business tools reviews for 120+ industries.
        Find the best solutions for agriculture, automotive, healthcare, construction, and more.
        Free your business with the right tools.
      </p>
      </header>

      <ArticleList pages={pages} categories={categories} language="en-US" />
    </div>
  )
}