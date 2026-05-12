import type { Metadata } from 'next'
import Script from 'next/script'
import { Header } from '@/components/Header'
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
    icon: [
      { url: '/favicon-48.png', type: 'image/png', sizes: '48x48' },
      { url: '/favicon-32.png', type: 'image/png', sizes: '32x32' },
      { url: '/favicon-16.png', type: 'image/png', sizes: '16x16' },
      { url: '/icon.webp', type: 'image/webp' },
    ],
    apple: [{ url: '/icon.png', type: 'image/png', sizes: '1024x1024' }],
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
        <Header />
        {/* Google AdSense */}
        <Script
          async
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9920271435480805"
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />

        {/* 百度统计 */}
        <Script id="baidu-analytics" strategy="afterInteractive">
          {`
            var _hmt = _hmt || [];
            (function() {
              var hm = document.createElement("script");
              hm.src = "https://hm.baidu.com/hm.js?4193c918286513f395709d49d19df88d";
              var s = document.getElementsByTagName("script")[0];
              s.parentNode.insertBefore(hm, s);
            })();
          `}
        </Script>
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