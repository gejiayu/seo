import { NextRequest, NextResponse } from 'next/server'
import { getAllPagesList } from '@/lib/data-loader'

export const runtime = 'nodejs'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '50')
  const category = searchParams.get('category') || undefined
  const language = (searchParams.get('language') || 'en-US') as 'en-US' | 'zh-CN'

  const allPages = getAllPagesList(language)

  // Filter by category if provided
  const filteredPages = category
    ? allPages.filter(p => p.category === category)
    : allPages

  // Pagination
  const startIndex = (page - 1) * limit
  const endIndex = startIndex + limit
  const pages = filteredPages.slice(startIndex, endIndex)

  return NextResponse.json({
    pages,
    total: filteredPages.length,
    page,
    limit,
    hasMore: endIndex < filteredPages.length,
    categories: Array.from(new Set(allPages.map(p => p.category))).sort(),
  })
}