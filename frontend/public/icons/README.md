# PWA Icons for Richy's Board

This directory contains app icons in various sizes for Progressive Web App (PWA) installation across different devices and platforms.

## Required Icon Sizes

The following icon sizes are required for full PWA compatibility:

- **72x72** - Android small icon
- **96x96** - Android medium icon, desktop shortcuts
- **128x128** - Chrome Web Store
- **144x144** - Microsoft Windows tile
- **152x152** - iOS home screen (iPad)
- **192x192** - Android home screen (standard)
- **384x384** - Android splash screen
- **512x512** - Android home screen (high-res), splash screens

## How to Generate Icons

### Option 1: Using an Online Tool (Easiest)

1. Create a single high-resolution logo (1024x1024 PNG recommended)
2. Visit one of these online PWA icon generators:
   - https://realfavicongenerator.net/
   - https://www.pwabuilder.com/imageGenerator
   - https://progressier.com/pwa-icons-and-ios-splash-screen-generator

3. Upload your logo and download the generated icons
4. Place all generated icons in this `icons/` directory

### Option 2: Using ImageMagick (Command Line)

If you have ImageMagick installed:

```bash
# From your base logo (logo.png)
convert logo.png -resize 72x72 icon-72x72.png
convert logo.png -resize 96x96 icon-96x96.png
convert logo.png -resize 128x128 icon-128x128.png
convert logo.png -resize 144x144 icon-144x144.png
convert logo.png -resize 152x152 icon-152x152.png
convert logo.png -resize 192x192 icon-192x192.png
convert logo.png -resize 384x384 icon-384x384.png
convert logo.png -resize 512x512 icon-512x512.png
```

### Option 3: Using Node.js Script

Create a script `generate-icons.js`:

```javascript
const sharp = require('sharp');
const fs = require('fs');

const sizes = [72, 96, 128, 144, 152, 192, 384, 512];
const inputFile = 'logo.png'; // Your source logo

sizes.forEach(size => {
  sharp(inputFile)
    .resize(size, size)
    .toFile(`icon-${size}x${size}.png`)
    .then(() => console.log(`Generated ${size}x${size}`))
    .catch(err => console.error(err));
});
```

Then run:
```bash
npm install sharp
node generate-icons.js
```

## Design Guidelines

### Logo Requirements
- **Format**: PNG with transparency
- **Dimensions**: 1024x1024px (will be resized)
- **Padding**: Leave 10-15% padding around the logo for safe area
- **Content**: Avoid fine details that won't be visible at small sizes
- **Colors**: Use brand colors, ensure good contrast

### Icon Best Practices
- Use a simple, recognizable symbol
- Avoid text in icons smaller than 192x192
- Test icons on both light and dark backgrounds
- Ensure icons are readable at the smallest size (72x72)
- Use consistent styling across all sizes

## Placeholder Icons

Until you generate your own icons, the app will use the Vite default icons. To replace them:

1. Generate your icon set using one of the methods above
2. Place all icons in this directory
3. Verify the filenames match those in `/manifest.json`
4. Test the installation on mobile devices

## Testing Icons

### Desktop
1. Open DevTools (F12)
2. Go to Application > Manifest
3. Verify all icons are loaded correctly

### Mobile
1. Add the app to home screen
2. Check the icon appearance
3. Open the app and verify splash screen

## Additional Files

Don't forget to also create:
- **favicon.ico** - For browser tabs
- **apple-touch-icon.png** - For iOS (180x180)
- Splash screens for iOS (various sizes)

## Resources

- [PWA Icon Requirements](https://web.dev/add-manifest/)
- [Apple Icon Guidelines](https://developer.apple.com/design/human-interface-guidelines/ios/icons-and-images/app-icon/)
- [Android Icon Guidelines](https://developer.android.com/guide/practices/ui_guidelines/icon_design_launcher)
