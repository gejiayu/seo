import type { Metadata } from 'next'
import Script from 'next/script'
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
        {/* Google AdSense Ownership Verification */}
        <meta name="google-adsense-account" content="ca-pub-9920271435480805" />
      </head>
      <body className="antialiased">
        {/* Google AdSense */}
        <Script
          async
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9920271435480805"
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />
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
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
        <footer className="bg-gray-100 border-t border-gray-200 py-8 mt-12">
          <div className="max-w-4xl mx-auto px-6">
            <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-600">
              <a href="/about-us" className="hover:text-gray-900 transition-colors">About Us</a>
              <a href="/privacy-policy" className="hover:text-gray-900 transition-colors">Privacy Policy</a>
              <a href="/terms-of-service" className="hover:text-gray-900 transition-colors">Terms of Service</a>
            </div>
            <div className="text-center text-gray-500 text-xs mt-4">
              © 2026 housecar.life - Remote Work Tools & Productivity Research
            </div>
          </div>
        </footer>
      </body>
    </html>
  )
}