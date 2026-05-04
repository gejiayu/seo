const fs = require('fs');
const path = require('path');

const directories = [
  'data/agricultural-farming-rental-tools',
  'data/bike-cycling-rental-tools',
  'data/boat-marine-rental-tools',
  'data/camera-photography-rental-tools',
  'data/camping-outdoor-gear-rental-tools',
  'data/car-vehicle-rental-tools',
  'data/zh/agricultural-farming-rental-tools',
  'data/zh/bike-cycling-rental-tools',
  'data/zh/boat-marine-rental-tools',
  'data/zh/camera-photography-rental-tools',
  'data/zh/camping-outdoor-gear-rental-tools',
  'data/zh/car-vehicle-rental-tools'
];

let totalProcessed = 0;
let totalTruncated = 0;
let errors = [];

function truncateDescription(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);

    if (!data.description) {
      return { processed: true, truncated: false };
    }

    if (data.description.length > 155) {
      const originalLength = data.description.length;
      data.description = data.description.substring(0, 152) + '...';

      fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');

      return {
        processed: true,
        truncated: true,
        originalLength,
        newLength: data.description.length
      };
    }

    return { processed: true, truncated: false };
  } catch (err) {
    return { processed: false, error: err.message };
  }
}

directories.forEach(dir => {
  if (!fs.existsSync(dir)) {
    console.log(`Directory not found: ${dir}`);
    return;
  }

  const files = fs.readdirSync(dir).filter(f => f.endsWith('.json'));

  files.forEach(file => {
    const filePath = path.join(dir, file);
    const result = truncateDescription(filePath);

    if (result.error) {
      errors.push({ file: filePath, error: result.error });
    } else if (result.processed) {
      totalProcessed++;
      if (result.truncated) {
        totalTruncated++;
        console.log(`Truncated: ${filePath} (${result.originalLength} -> ${result.newLength} chars)`);
      }
    }
  });
});

console.log('\n=== Summary ===');
console.log(`Total processed: ${totalProcessed}`);
console.log(`Total truncated: ${totalTruncated}`);
console.log(`Errors: ${errors.length}`);

if (errors.length > 0) {
  console.log('\nErrors:');
  errors.forEach(e => console.log(`  ${e.file}: ${e.error}`));
}
