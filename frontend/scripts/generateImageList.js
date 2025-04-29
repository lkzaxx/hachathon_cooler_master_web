const fs = require('fs');
const path = require('path');

const imageDir = path.join(__dirname, '../public/img/Computer_Case');
const outputFile = path.join(__dirname, '../src/computerCaseImages.json');

try {
    const files = fs.readdirSync(imageDir);
    // 過濾掉非圖片文件 (可選，根據需要調整後綴名)
    const imageFiles = files.filter(file => /\.(png|jpe?g|gif|webp)$/i.test(file));

    fs.writeFileSync(outputFile, JSON.stringify(imageFiles, null, 2));
    console.log(`Successfully generated image list at ${outputFile}`);
} catch (err) {
    console.error('Error generating image list:', err);
    // 寫入空數組以防錯誤導致後續導入失敗
    fs.writeFileSync(outputFile, JSON.stringify([], null, 2));
} 