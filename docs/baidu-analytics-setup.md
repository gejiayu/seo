# 百度统计配置指南 - housecar.life

## ✅ 已完成步骤

1. [x] 百度统计代码已添加到 `src/app/layout.tsx`（第65-75行）
2. [x] 与Google AdSense共存，不会冲突

## 🔜 待完成步骤（5分钟）

### 1️⃣ 在百度统计创建站点

访问：https://tongji.baidu.com/web/welcome/login

输入信息：

| 项目 | 内容 |
|------|------|
| 站点名称 | `HouseCar` |
| 站点域名 | `www.housecar.life` |
| 网站首页 | `https://www.housecar.life` |

### 2️⃣ 获取站点ID

创建成功后，百度会显示站点ID（类似：`a1b2c3d4e5f6g7h8`）

**复制这个ID**

### 3️⃣ 替换代码中的ID

打开 `src/app/layout.tsx`，找到第69行：

```tsx
hm.src = "https://hm.baidu.com/hm.js?YOUR_SITE_ID"; // 替换为百度统计站点ID
```

替换为：

```tsx
hm.src = "https://hm.baidu.com/hm.js?a1b2c3d4e5f6g7h8"; // 你的真实站点ID
```

### 4️⃣ 本地测试

```bash
cd /Users/gejiayu/owner/seo
npm run dev
```

访问 http://localhost:3000，查看浏览器控制台是否有百度统计请求。

### 5️⃣ 部署到生产环境

```bash
npm run build
npm run start
```

或推送代码到部署平台（Vercel/Netlify等）。

### 6️⃣ 验证成功

等待5分钟后，访问百度统计后台查看数据。

---

## 📊 代码位置

百度统计代码位置：`src/app/layout.tsx` 第65-75行

```tsx
{/* 百度统计 */}
<Script id="baidu-analytics" strategy="afterInteractive">
  {`
    var _hmt = _hmt || [];
    (function() {
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?YOUR_SITE_ID";
      var s = document.getElementsByTagName("script")[0];
      s.parentNode.insertBefore(hm, s);
    })();
  `}
</Script>
```

---

## 🎯 Legal Shield应用配置

站点ID是通用的！同一个ID可以用于：

1. ✅ **housecar.life网站**（已添加）
2. ✅ **Legal Shield应用**（待添加）

**Legal Shield配置步骤：**

拿到站点ID后，还需要修改：

1. `zchxz/index.html`（第13行）
2. `legal-shield/electron/analytics.js`（第6行）

---

## 🔧 部署平台确认

**问题：你的网站部署在哪里？**

- Vercel？
- Netlify？
- Cloudflare Pages？
- 其他？

推送代码后，部署平台会自动更新。

---

## 📝 下一步操作清单

| 步骤 | 操作 | 预计时间 |
|------|------|---------|
| ✅ 添加百度统计代码 | 已完成 | 0分钟 |
| 🔜 百度统计创建站点 | 你操作 | 2分钟 |
| 🔜 获取站点ID | 复制 | 1分钟 |
| 🔜 替换代码ID | 编辑 | 1分钟 |
| 🔜 推送代码部署 | git push | 1分钟 |
| 🔜 配置Legal Shield | 替换两处 | 1分钟 |
| 🔜 验证成功 | 等待5分钟 | 5分钟 |
| **总计** | - | **约10分钟** |

---

## 🚀 现在请操作

**第1步：去百度统计创建站点**
- 站点域名：`www.housecar.life`
- 网站首页：`https://www.housecar.life`

**第2步：获取站点ID后告诉我**

我帮你：
1. 替换代码中的ID
2. 掄送代码到部署平台
3. 配置Legal Shield应用

等你消息！ 🎯