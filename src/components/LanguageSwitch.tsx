'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface LanguageSwitchProps {
  currentLanguage: 'en-US' | 'zh-CN'
  alternateUrl?: string // For article pages
}

export function LanguageSwitch({ currentLanguage, alternateUrl }: LanguageSwitchProps) {
  const pathname = usePathname()

  // Determine the target URL
  const getTargetUrl = (): string => {
    if (alternateUrl) {
      return alternateUrl
    }

    // For homepage or category pages
    if (currentLanguage === 'en-US') {
      // English to Chinese: add /zh prefix
      if (pathname === '/') {
        return '/zh'
      }
      return `/zh${pathname}`
    } else {
      // Chinese to English: remove /zh prefix
      if (pathname === '/zh') {
        return '/'
      }
      return pathname.replace('/zh', '') || '/'
    }
  }

  const targetUrl = getTargetUrl()
  const targetLanguage = currentLanguage === 'en-US' ? 'zh-CN' : 'en-US'

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-500">Language:</span>
      <Link
        href={targetUrl}
        className="px-3 py-1.5 rounded-md text-sm font-medium bg-gray-100 hover:bg-gray-200 transition-colors"
      >
        {targetLanguage === 'zh-CN' ? '中文' : 'EN'}
      </Link>
    </div>
  )
}