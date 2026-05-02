'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function Header() {
  const pathname = usePathname()
  const isZh = pathname.startsWith('/zh')

  const switchUrl = isZh
    ? pathname.replace('/zh', '') || '/'
    : `/zh${pathname === '/' ? '' : pathname}`

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href={isZh ? '/zh' : '/'} className="text-xl font-bold text-gray-900">
          HouseCar
        </Link>

        <nav className="flex items-center gap-4">
          <Link
            href={switchUrl}
            className="px-3 py-1.5 rounded-md text-sm font-medium bg-gray-100 hover:bg-gray-200 transition-colors"
          >
            {isZh ? 'EN' : '中文'}
          </Link>
        </nav>
      </div>
    </header>
  )
}