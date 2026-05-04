const fs = require('fs');
const path = require('path');

const MAX_DESC_LENGTH = 155;

function truncateDescription(description) {
  if (!description) return description;
  if (description.length <= MAX_DESC_LENGTH) return description;

  // 找到155字符附近最近的空格（往前找），保留单词边界
  const truncated = description.substring(0, MAX_DESC_LENGTH);
  const lastSpace = truncated.lastIndexOf(' ');

  if (lastSpace > 0) {
    return truncated.substring(0, lastSpace) + '...';
  } else {
    return truncated + '...';
  }
}

function processFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const json = JSON.parse(content);

    const originalDesc = json.description;
    const truncatedDesc = truncateDescription(originalDesc);

    if (originalDesc !== truncatedDesc) {
      json.description = truncatedDesc;
      fs.writeFileSync(filePath, JSON.stringify(json, null, 2), 'utf8');
      return { processed: true, originalLength: originalDesc.length, newLength: truncatedDesc.length };
    }

    return { processed: false };
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
    return { error: true };
  }
}

function processDirectory(directory) {
  const files = fs.readdirSync(directory).filter(file => file.endsWith('.json'));

  let stats = {
    total: files.length,
    processed: 0,
    skipped: 0,
    errors: 0
  };

  for (const file of files) {
    const filePath = path.join(directory, file);
    const result = processFile(filePath);

    if (result.error) {
      stats.errors++;
    } else if (result.processed) {
      stats.processed++;
    } else {
      stats.skipped++;
    }
  }

  return stats;
}

// 处理三个目录
const directories = [
  'data/customer-support-tools',
  'data/warehouse-inventory-tools',
  'data/transportation-fleet-tools'
];

const zhDirectories = [
  'data/zh/customer-support-tools',
  'data/zh/warehouse-inventory-tools',
  'data/zh/transportation-fleet-tools'
];

console.log('Processing English directories...\n');

let totalStats = {
  total: 0,
  processed: 0,
  skipped: 0,
  errors: 0
};

for (const dir of directories) {
  const stats = processDirectory(dir);
  console.log(`${dir}:`);
  console.log(`  Total: ${stats.total}`);
  console.log(`  Processed: ${stats.processed}`);
  console.log(`  Skipped: ${stats.skipped}`);
  console.log(`  Errors: ${stats.errors}\n`);

  totalStats.total += stats.total;
  totalStats.processed += stats.processed;
  totalStats.skipped += stats.skipped;
  totalStats.errors += stats.errors;
}

console.log('Processing Chinese (zh) directories...\n');

for (const dir of zhDirectories) {
  if (fs.existsSync(dir)) {
    const stats = processDirectory(dir);
    console.log(`${dir}:`);
    console.log(`  Total: ${stats.total}`);
    console.log(`  Processed: ${stats.processed}`);
    console.log(`  Skipped: ${stats.skipped}`);
    console.log(`  Errors: ${stats.errors}\n`);

    totalStats.total += stats.total;
    totalStats.processed += stats.processed;
    totalStats.skipped += stats.skipped;
    totalStats.errors += stats.errors;
  } else {
    console.log(`${dir}: Directory not found\n`);
  }
}

console.log('====================');
console.log('Total Summary:');
console.log(`  Total files: ${totalStats.total}`);
console.log(`  Processed: ${totalStats.processed}`);
console.log(`  Skipped: ${totalStats.skipped}`);
console.log(`  Errors: ${totalStats.errors}`);