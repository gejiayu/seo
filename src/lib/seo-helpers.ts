/**
 * SEO helper utilities
 */

/**
 * Truncates description to 150-160 characters for meta description
 * Preserves word boundaries and adds ellipsis
 */
export function truncateDescription(description: string, maxLength = 155): string {
  if (description.length <= maxLength) return description

  const truncated = description.substring(0, maxLength)
  const lastSpace = truncated.lastIndexOf(' ')

  if (lastSpace === -1) return truncated + '...'

  return truncated.substring(0, lastSpace) + '...'
}

/**
 * Generates OG image URL
 */
export function generateOgImage(title: string, category?: string): string {
  const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'
  const params = new URLSearchParams({ title: title.slice(0, 60) })
  if (category) params.append('category', category)
  return `${siteUrl}/api/og?${params.toString()}`
}

/**
 * Formats category name for display
 */
export function formatCategoryName(category: string): string {
  return category
    .replace(/-/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
}