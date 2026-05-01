import fs from 'fs'
import path from 'path'

// Lightweight interface for list display (excludes heavy content field)
export interface PageListItem {
  title: string
  description: string
  seo_keywords: string[]
  category: string
  slug: string
  published_at?: string
  author?: string
}

export interface PageData extends PageListItem {
  content: string
}

interface PageInfo {
  category: string
  slug: string
  data: PageData
}

const dataDirectory = path.join(process.cwd(), 'data')

function walkDirectory(dir: string, pages: PageInfo[]): void {
  if (!fs.existsSync(dir)) {
    return
  }

  const files = fs.readdirSync(dir)

  for (const file of files) {
    const filePath = path.join(dir, file)
    const stat = fs.statSync(filePath)

    if (stat.isDirectory()) {
      walkDirectory(filePath, pages)
    } else if (file.endsWith('.json')) {
      try {
        const content = fs.readFileSync(filePath, 'utf8')
        const data: PageData = JSON.parse(content)

        // Calculate category and slug from file path
        const relativePath = path.relative(dataDirectory, filePath)
        const pathParts = relativePath.split(path.sep)

        // Extract category from directory structure
        const category = pathParts.length > 1 ? pathParts[0] : 'uncategorized'

        // Use slug from data or derive from filename
        const filenameSlug = path.basename(file, '.json')
        const slug = data.slug || filenameSlug

        pages.push({
          category,
          slug,
          data: { ...data, category, slug },
        })
      } catch (error) {
        console.error(`Error parsing JSON file ${filePath}:`, error)
      }
    }
  }
}

export function getAllPages(): PageInfo[] {
  const pages: PageInfo[] = []
  walkDirectory(dataDirectory, pages)
  return pages
}

// Lightweight version for list display - excludes heavy content field
export function getAllPagesList(): PageListItem[] {
  const pages = getAllPages()
  return pages.map((p) => ({
    title: p.data.title,
    description: p.data.description,
    seo_keywords: p.data.seo_keywords,
    category: p.data.category,
    slug: p.data.slug,
    published_at: p.data.published_at,
    author: p.data.author,
  }))
}

export function getPageByCategoryAndSlug(category: string, slug: string): PageData | null {
  const pages = getAllPages()
  const page = pages.find(
    (p) => p.category === category && p.slug === slug
  )
  return page?.data || null
}

export function getPagesByCategory(category: string): PageInfo[] {
  const pages = getAllPages()
  return pages.filter((p) => p.category === category)
}

export function getAllCategories(): string[] {
  const pages = getAllPages()
  const categories = new Set(pages.map((p) => p.category))
  return Array.from(categories).sort()
}

export function getAllPagePaths(): Array<{ category: string; slug: string }> {
  const pages = getAllPages()
  return pages.map((p) => ({
    category: p.category,
    slug: p.slug,
  }))
}