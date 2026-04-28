import type { Metadata } from 'next'
import Script from 'next/script'
import './globals.css'

export const metadata: Metadata = {
  title: {
    default: 'SEO Content Hub',
    template: '%s | SEO Content Hub',
  },
  description: 'Programmatic SEO content pages generated from structured data',
}

// WebSite Schema for entire site
const siteUrl = process.env.SITE_URL || 'https://example.com'
const websiteSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'SEO Content Hub',
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
  name: 'SEO Content Hub',
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
        {/* WebSite Schema */}
        <Script
          id="website-schema"
          type="application/ld+json"
          strategy="beforeInteractive"
        >
          {JSON.stringify(websiteSchema)}
        </Script>
        {/* Organization Schema */}
        <Script
          id="organization-schema"
          type="application/ld+json"
          strategy="beforeInteractive"
        >
          {JSON.stringify(organizationSchema)}
        </Script>
      </head>
      <body className="antialiased">
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
      </body>
    </html>
  )
}