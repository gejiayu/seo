import { Metadata } from 'next'
import { getAllPages, getAllCategories } from '@/lib/data-loader'
import { ArticleList } from '@/components/ArticleList'

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

      <ArticleList pages={pages} categories={categories} />
    </div>
  )
}