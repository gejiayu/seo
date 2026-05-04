
// 中文版footer组件
function ZhFooter() {
  return (
    <footer className="bg-gray-100 border-t border-gray-200 py-8 mt-12">
      <div className="max-w-4xl mx-auto px-6">
        <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-600">
          <a href="/zh/about-us" className="hover:text-gray-900 transition-colors">关于我们</a>
          <a href="/zh/privacy-policy" className="hover:text-gray-900 transition-colors">隐私政策</a>
          <a href="/zh/terms-of-service" className="hover:text-gray-900 transition-colors">服务条款</a>
          <a href="/" className="hover:text-gray-900 transition-colors">English</a>
        </div>
        <div className="text-center text-gray-500 text-xs mt-4">
          © 2026 housecar.life - 远程工作工具与生产力研究
        </div>
      </div>
    </footer>
  )
}

export default function ZhLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <main className="min-h-screen bg-gray-50">
        {children}
      </main>
      <ZhFooter />
    </>
  )
}