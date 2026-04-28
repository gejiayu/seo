# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **Programmatic SEO (pSEO)** project built with Next.js 14 App Router. Generates SEO-optimized pages from JSON data files, enabling scalable content creation without manual page authoring.

## Commands

```bash
npm run dev          # Start dev server on http://localhost:3000
npm run build        # Build for production + generate sitemap
npm run start        # Start production server
npm run lint         # Run ESLint checks
```

## Architecture

### Data-Driven Page Generation

1. **Data Layer** (`data/` directory)
   - JSON files in subdirectories by category
   - Each file: `title`, `description`, `content`, `seo_keywords`, `slug`
   - Category derived from directory (e.g., `data/remote-tools/file.json` → category: `remote-tools`)

2. **Data Loader** (`src/lib/data-loader.ts`)
   - `getAllPages()` - All pages with category/slug metadata
   - `getPageByCategoryAndSlug(category, slug)` - Single page
   - `getAllPagePaths()` - Paths for `generateStaticParams`

3. **Routing**
   - Homepage: `/` → Lists all pages (`src/app/page.tsx`)
   - Articles: `/posts/[slug]` → Single article (`src/app/posts/[slug]/page.tsx`)
   - SSG via `generateStaticParams()`

### SEO Implementation

- **Metadata**: OpenGraph, Twitter cards, canonical URLs
- **JSON-LD**: Static SSR rendering using `dangerouslySetInnerHTML` (not Next.js Script component)
- **Sitemap**: Auto-generated via `next-sitemap` postbuild hook

### JSON-LD Schema Types

- Homepage: `WebSite` + `Organization` (no rich results, just base info)
- Articles: `Article` schema (produces rich results in Google)

## Adding New Content

1. Create JSON in `data/<category>/<slug>.json`:
   ```json
   {
     "title": "Title",
     "description": "150-160 char description",
     "content": "Markdown-like content",
     "seo_keywords": ["keyword1", "keyword2"],
     "slug": "url-slug",
     "published_at": "2024-01-20",
     "author": "Author"
   }
   ```
2. Run `npm run build`

## Content Format

- `# Heading` → `<h1>`
- `## Heading` → `<h2>`
- `- item` → `<ul><li>`
- `1. item` → `<ol><li>`
- `\n\n` separated text → `<p>`

## Environment Variables

- `SITE_URL` - Production URL for sitemap and JSON-LD (default: `https://www.housecar.life`)