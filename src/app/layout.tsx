import type { Metadata } from 'next'
import './globals.css'

const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: 'HouseCar',
    template: '%s | HouseCar',
  },
  description: 'Programmatic SEO content pages generated from structured data',
}

// WebSite Schema for entire site
const websiteSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'HouseCar',
  url: siteUrl,
  description: 'Programmatic SEO content pages generated from structured data',
  potentialAction: {
    '@type': 'SearchAction',
    target: `${siteUrl}/search?q={search_term_string}`,
    'query-input': 'required name=search_term_string',
  },
}

// Organization Schema
const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'HouseCar',
  url: siteUrl,
  logo: `${siteUrl}/logo.png`,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* WebSite Schema - SSR rendered */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(websiteSchema),
          }}
        />
        {/* Organization Schema - SSR rendered */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(organizationSchema),
          }}
        />
      </head>
      <body className="antialiased">
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
      </body>
    </html>
  )
}