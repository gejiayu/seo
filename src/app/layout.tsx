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
  icons: {
    icon: '/icon.png',
    apple: '/icon.png',
  },
}

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
        <meta name="google-adsense-account" content="ca-pub-9920271435480805" />
      </head>
      <body className="antialiased">
        <Script
          async
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9920271435480805"
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />
        <Script id="website-schema" type="application/ld+json" strategy="beforeInteractive">
          {JSON.stringify(websiteSchema)}
        </Script>
        <Script id="organization-schema" type="application/ld+json" strategy="beforeInteractive">
          {JSON.stringify(organizationSchema)}
        </Script>
        {children}
      </body>
    </html>
  )
}