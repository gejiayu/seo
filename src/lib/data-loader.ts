import fs from 'fs'
import path from 'path'

// Language type
export type Language = 'en-US' | 'zh-CN'

// Lightweight interface for list display (excludes heavy content field)
export interface PageListItem {
  title: string
  description: string
  seo_keywords: string[]
  category: string
  slug: string
  published_at?: string
  author?: string
  language?: Language
}

export interface PageData extends PageListItem {
  content: string
  canonical_link?: string
  alternate_links?: Record<Language, string>
}

interface PageInfo {
  category: string
  slug: string
  data: PageData
}

const dataDirectory = path.join(process.cwd(), 'data')

// Get data directory based on language
function getDataDirectory(language: Language): string {
  if (language === 'zh-CN') {
    return path.join(dataDirectory, 'zh')
  }
  return dataDirectory // English is in root data directory
}

function walkDirectory(dir: string, pages: PageInfo[], language: Language): void {
  if (!fs.existsSync(dir)) {
    return
  }

  const files = fs.readdirSync(dir)

  for (const file of files) {
    const filePath = path.join(dir, file)
    const stat = fs.statSync(filePath)

    // Skip zh directory when processing English
    if (stat.isDirectory()) {
      if (language === 'en-US' && file === 'zh') {
        continue // Skip zh subdirectory for English mode
      }
      walkDirectory(filePath, pages, language)
    } else if (file.endsWith('.json')) {
      try {
        const content = fs.readFileSync(filePath, 'utf8')
        const data: PageData = JSON.parse(content)

        // Verify language matches requested language
        if (data.language && data.language !== language) {
          continue // Skip files with wrong language tag
        }

        // Calculate category and slug from file path
        const relativePath = path.relative(dir.includes('/zh/') ? path.join(dataDirectory, 'zh') : dataDirectory, filePath)
        const pathParts = relativePath.split(path.sep)

        // Extract category from directory structure
        const category = pathParts.length > 1 ? pathParts[0] : 'uncategorized'

        // Use slug from data or derive from filename
        const filenameSlug = path.basename(file, '.json')
        const slug = data.slug || filenameSlug

        pages.push({
          category,
          slug,
          data: { ...data, category, slug, language },
        })
      } catch (error) {
        console.error(`Error parsing JSON file ${filePath}:`, error)
      }
    }
  }
}

export function getAllPages(language: Language = 'en-US'): PageInfo[] {
  const pages: PageInfo[] = []
  const targetDir = getDataDirectory(language)
  walkDirectory(targetDir, pages, language)
  return pages
}

// Lightweight version for list display - excludes heavy content field
export function getAllPagesList(language: Language = 'en-US'): PageListItem[] {
  const pages = getAllPages(language)
  return pages.map((p) => ({
    title: p.data.title,
    description: p.data.description,
    seo_keywords: p.data.seo_keywords,
    category: p.data.category,
    slug: p.data.slug,
    published_at: p.data.published_at,
    author: p.data.author,
    language: p.data.language,
  }))
}

export function getPageByCategoryAndSlug(category: string, slug: string, language: Language = 'en-US'): PageData | null {
  const pages = getAllPages(language)
  const page = pages.find(
    (p) => p.category === category && p.slug === slug
  )
  return page?.data || null
}

export function getPageBySlug(slug: string, language: Language = 'en-US'): PageData | null {
  const pages = getAllPages(language)
  return pages.find((p) => p.slug === slug)?.data || null
}

export function getPagesByCategory(category: string, language: Language = 'en-US'): PageInfo[] {
  const pages = getAllPages(language)
  return pages.filter((p) => p.category === category)
}

export function getAllCategories(language: Language = 'en-US'): string[] {
  const pages = getAllPages(language)
  const categories = new Set(pages.map((p) => p.category))
  return Array.from(categories).sort()
}

export function getAllPagePaths(language: Language = 'en-US'): Array<{ category: string; slug: string }> {
  const pages = getAllPages(language)
  return pages.map((p) => ({
    category: p.category,
    slug: p.slug,
  }))
}