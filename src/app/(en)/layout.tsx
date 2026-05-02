import { Header } from '@/components/Header'

// 英文版footer组件
function EnFooter() {
  return (
    <footer className="bg-gray-100 border-t border-gray-200 py-8 mt-12">
      <div className="max-w-4xl mx-auto px-6">
        <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-600">
          <a href="/about-us" className="hover:text-gray-900 transition-colors">About Us</a>
          <a href="/privacy-policy" className="hover:text-gray-900 transition-colors">Privacy Policy</a>
          <a href="/terms-of-service" className="hover:text-gray-900 transition-colors">Terms of Service</a>
          <a href="/zh" className="hover:text-gray-900 transition-colors">中文</a>
        </div>
        <div className="text-center text-gray-500 text-xs mt-4">
          © 2026 housecar.life - Remote Work Tools & Productivity Research
        </div>
      </div>
    </footer>
  )
}

export default function EnLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <Header />
      <main className="min-h-screen bg-gray-50">
        {children}
      </main>
      <EnFooter />
    </>
  )
}