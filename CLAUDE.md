# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Programmatic SEO (pSEO)** project built with Next.js 14 App Router. It generates SEO-optimized pages dynamically from JSON data files, enabling scalable content creation without manual page authoring.

## Commands

```bash
# Development
npm run dev          # Start dev server on http://localhost:3000

# Build & Production
npm run build        # Build for production + generate sitemap
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint checks
```

## Architecture

### Data-Driven Page Generation

The project uses a **data-first architecture**:

1. **Data Layer** (`data/` directory)
   - JSON files organized in subdirectories by category
   - Each JSON file represents one page with: `title`, `description`, `content`, `seo_keywords`, `slug`
   - Category is derived from the directory structure (e.g., `data/test/hello-world.json` → category: `test`, slug: `hello-world`)

2. **Data Loader** (`src/lib/data-loader.ts`)
   - `getAllPages()` - Returns all pages with category/slug metadata
   - `getPageByCategoryAndSlug(category, slug)` - Get single page data
   - `getPagesByCategory(category)` - Filter pages by category
   - `getAllCategories()` - List all categories
   - `getAllPagePaths()` - Get paths for `generateStaticParams`

3. **Routing** (`src/app/[category]/[slug]/page.tsx`)
   - Dynamic route segments: `/[category]/[slug]`
   - `generateStaticParams()` pre-generates all pages at build time
   - `generateMetadata()` creates SEO metadata per page (title, description, keywords, OpenGraph, Twitter cards)
   - Includes JSON-LD Article schema for structured data
   - Returns 404 if page data not found

4. **Homepage** (`src/app/page.tsx`)
   - Lists all available pages with category badges, titles, descriptions
   - Shows keyword tags for each page

### Runtime Configuration

Both pages use Node.js runtime for filesystem access:
```typescript
export const runtime = 'nodejs'
```

The dynamic page also has:
```typescript
export const dynamic = 'force-dynamic'
export const dynamicParams = true
```

### SEO Features

- **Metadata**: Full SEO metadata per page including OpenGraph/Twitter cards
- **JSON-LD**: Article schema structured data for search engines
- **Sitemap**: Auto-generated via `next-sitemap` in `postbuild` script
- **Robots.txt**: Auto-generated with `/api/*` exclusion
- **Canonical URLs**: Set in metadata for each page

### Key Files

| Path | Purpose |
|------|---------|
| `src/lib/data-loader.ts` | Recursive JSON data loader with filesystem traversal |
| `src/app/[category]/[slug]/page.tsx` | Dynamic page component with SEO metadata and JSON-LD |
| `src/app/page.tsx` | Homepage listing all pages |
| `next-sitemap.config.js` | Sitemap/robots.txt configuration |

## Adding New Pages

1. Create a JSON file in the appropriate category directory:
   ```bash
   mkdir -p data/your-category
   ```
2. Create `data/your-category/your-slug.json`:
   ```json
   {
     "title": "Your Page Title",
     "description": "Meta description (150-160 chars ideal)",
     "content": "Markdown-like content with ## headings and bullet lists",
     "seo_keywords": ["keyword1", "keyword2", "keyword3"],
     "slug": "your-slug",
     "published_at": "2024-01-20",
     "author": "Author Name"
   }
   ```
3. Run `npm run build` to regenerate static pages and sitemap

## Content Format

The `content` field supports simple markdown-like syntax:
- `# Heading 1` → `<h1>`
- `## Heading 2` → `<h2>`
- `- List item` → `<ul><li>`
- `1. Numbered item` → `<ol><li>`
- Plain text separated by `\n\n` → `<p>`

## Environment Variables

Set `SITE_URL` in production to configure the sitemap base URL and JSON-LD URLs:
```bash
SITE_URL=https://your-domain.com npm run build
```

Defaults to `https://example.com` if not set.