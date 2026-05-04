# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **Programmatic SEO (pSEO)** project built with Next.js 14 App Router with i18n support (English/Chinese). Generates SEO-optimized pages from JSON data files, enabling scalable content creation without manual page authoring.

## Commands

```bash
npm run dev          # Start dev server on http://localhost:3000
npm run build        # Build for production + generate sitemap
npm run start        # Start production server
npm run lint         # Run ESLint checks
```

## Architecture

### i18n Routing (Route Groups)

- **English** (default): Route group `(en)` - URLs without prefix (`/`, `/posts/[slug]`)
- **Chinese**: Route group `zh` - URLs with `/zh` prefix (`/zh`, `/zh/posts/[slug]`)
- Each language has its own layout with localized footer and language switcher

### Data-Driven Page Generation

1. **Data Layer** (`data/` directory)
   - English: `data/<category>/<slug>.json`
   - Chinese: `data/zh/<category>/<slug>.json`
   - Category derived from directory name

2. **Required JSON Fields**:
   ```json
   {
     "title": "string",
     "description": "string (150-160 chars for SEO)",
     "content": "HTML content (NOT Markdown)",
     "seo_keywords": ["keyword1", "keyword2"],  // MUST be array, NOT string
     "slug": "url-slug",
     "language": "en-US" | "zh-CN",
     "published_at": "2024-01-20",
     "author": "Author Name"
   }
   ```

3. **Critical: seo_keywords Format**
   - MUST be array of strings: `["k1", "k2"]`
   - NEVER comma-separated string: `"k1, k2"` (breaks SEO rendering)

4. **Data Loader** (`src/lib/data-loader.ts`)
   - `getAllPages(language)` - All pages with metadata
   - `getPageBySlug(slug, language)` - Single page lookup
   - `getAllPagePaths(language)` - Paths for `generateStaticParams`

### SEO Implementation

- **Metadata**: OpenGraph, Twitter cards, canonical URLs, hreflang alternates
- **JSON-LD**: Article + BreadcrumbList schemas (static SSR via `dangerouslySetInnerHTML`)
- **OG Images**: Dynamic generation via `/api/og` edge route
- **Sitemap**: Auto-generated in `src/app/sitemap.ts` (includes both languages)

### Supporting Libraries

- `src/lib/seo-helpers.ts` - Description truncation, OG image URL generation
- `src/lib/category-translations.ts` - 100+ category English→Chinese mappings

## Adding New Content

1. Create JSON in appropriate data directory:
   - English: `data/<category>/<slug>.json`
   - Chinese: `data/zh/<category>/<slug>.json`
2. Ensure `seo_keywords` is an array format
3. Run `npm run build` to regenerate sitemap

## Content Format

The `content` field is **raw HTML**, not Markdown:
- Headings: `<h1>`, `<h2>`, `<h3>`
- Lists: `<ul><li>`, `<ol><li>`
- Paragraphs: `<p>`
- Rendered via `dangerouslySetInnerHTML` in article template

## Environment Variables

- `SITE_URL` - Production URL (default: `https://www.housecar.life`)