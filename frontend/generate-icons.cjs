/**
 * PWA Icon Generator for Richy's Board
 *
 * This script generates all required PWA icons using Canvas
 * Run: node generate-icons.js
 */

const fs = require('fs');
const path = require('path');

// Check if canvas is available
let Canvas;
try {
  Canvas = require('canvas');
} catch (e) {
  console.log('\n⚠️  Canvas module not found. Installing it now...\n');
  console.log('Run: npm install canvas\n');
  console.log('Alternative: Use the HTML generator at public/icons/generate-placeholder-icons.html\n');
  process.exit(1);
}

const { createCanvas } = Canvas;

const sizes = [72, 96, 128, 144, 152, 192, 384, 512];
const outputDir = path.join(__dirname, 'public', 'icons');

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

function generateIcon(size) {
  const canvas = createCanvas(size, size);
  const ctx = canvas.getContext('2d');

  // Background gradient (blue)
  const gradient = ctx.createLinearGradient(0, 0, size, size);
  gradient.addColorStop(0, '#3b82f6');
  gradient.addColorStop(1, '#1d4ed8');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);

  // Add rounded corners effect
  const radius = size * 0.15;
  ctx.globalCompositeOperation = 'destination-in';
  ctx.beginPath();
  ctx.moveTo(radius, 0);
  ctx.lineTo(size - radius, 0);
  ctx.quadraticCurveTo(size, 0, size, radius);
  ctx.lineTo(size, size - radius);
  ctx.quadraticCurveTo(size, size, size - radius, size);
  ctx.lineTo(radius, size);
  ctx.quadraticCurveTo(0, size, 0, size - radius);
  ctx.lineTo(0, radius);
  ctx.quadraticCurveTo(0, 0, radius, 0);
  ctx.closePath();
  ctx.fill();

  // Reset composite operation
  ctx.globalCompositeOperation = 'source-over';

  // Draw "R" letter (main)
  ctx.fillStyle = 'white';
  ctx.font = `bold ${size * 0.6}px Arial`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('R', size / 2, size / 2);

  // Add "BOARD" text for larger icons
  if (size >= 192) {
    ctx.font = `bold ${size * 0.12}px Arial`;
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillText('BOARD', size / 2, size * 0.8);
  }

  return canvas;
}

console.log('🎨 Generating PWA Icons for Richy\'s Board...\n');

sizes.forEach(size => {
  const canvas = generateIcon(size);
  const filename = `icon-${size}x${size}.png`;
  const filepath = path.join(outputDir, filename);

  // Save as PNG
  const buffer = canvas.toBuffer('image/png');
  fs.writeFileSync(filepath, buffer);

  console.log(`✅ Generated: ${filename} (${(buffer.length / 1024).toFixed(2)} KB)`);
});

console.log('\n✨ All icons generated successfully!');
console.log(`📁 Location: ${outputDir}`);
console.log('\n📋 Next steps:');
console.log('1. Verify icons in /frontend/public/icons/');
console.log('2. Commit and push to Git');
console.log('3. Redeploy on Netlify');
console.log('4. Test PWA installation\n');
