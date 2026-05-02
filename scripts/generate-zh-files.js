const fs = require('fs');
const path = require('path');

const dataDir = '/Users/gejiayu/owner/seo/data';
const dirs = ['scooter-moped-rental-tools', 'portable-sanitation-rental-tools', 'medical-equipment-rental-tools'];

function generateZhFile(enFile) {
  const zhFile = enFile.replace('.json', '-zh.json');
  
  // Skip if zh file already exists
  if (fs.existsSync(zhFile)) return { skipped: true };
  
  try {
    const enData = JSON.parse(fs.readFileSync(enFile, 'utf8'));
    
    // Create zh data
    const zhData = {
      title: enData.title_cn || enData.title,
      description: enData.description_cn || enData.description,
      content: enData.content_cn || enData.content,
      seo_keywords: enData.seo_keywords_cn || enData.seo_keywords,
      slug: enData.slug + '-zh',
      published_at: enData.published_at,
      author: enData.author_cn || enData.author,
      language: 'zh-CN',
      canonical_link: `https://www.housecar.life/zh/posts/${enData.slug}-zh`,
      alternate_links: {
        'en-US': `https://www.housecar.life/posts/${enData.slug}`,
        'zh-CN': `https://www.housecar.life/zh/posts/${enData.slug}-zh`
      },
      category: enData.category
    };
    
    fs.writeFileSync(zhFile, JSON.stringify(zhData, null, 2));
    return { success: true, file: zhFile };
  } catch (err) {
    return { error: true, message: err.message, file: enFile };
  }
}

let results = { success: 0, skipped: 0, errors: [] };

dirs.forEach(dir => {
  const dirPath = path.join(dataDir, dir);
  const files = fs.readdirSync(dirPath)
    .filter(f => f.endsWith('.json') && !f.endsWith('-zh.json'))
    .map(f => path.join(dirPath, f));
  
  files.forEach(enFile => {
    const result = generateZhFile(enFile);
    if (result.skipped) results.skipped++;
    else if (result.success) results.success++;
    else results.errors.push(result);
  });
});

console.log(JSON.stringify(results, null, 2));
