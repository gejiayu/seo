import { Metadata } from 'next'
import HomePageClient from '@/components/HomePageClient'

export const runtime = 'nodejs'

const siteUrl = process.env.SITE_URL || 'https://www.housecar.life'

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: 'HouseCar.life - Business Tools & Software Comparison Guides | Free Your Business',
    description: 'Comprehensive software comparison guides and business tools reviews for 120+ industries. Find the best solutions for agriculture, automotive, healthcare, construction, and more. Free your business with the right tools.',
    alternates: {
      canonical: siteUrl,
      languages: {
        'en-US': siteUrl,
        'zh-CN': `${siteUrl}/zh`,
      },
    },
    openGraph: {
      title: 'HouseCar.life - Business Tools & Software Guides',
      description: 'Comprehensive software comparison guides and business tools reviews for 120+ industries. Free your business with the right tools.',
      url: siteUrl,
      type: 'website',
      siteName: 'HouseCar',
      locale: 'en_US',
    },
  }
}

export default function HomePage() {
  return <HomePageClient language="en-US" />
}