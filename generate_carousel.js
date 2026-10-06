const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.resolve(__dirname, 'carousel_cards');
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

const cards = [
  { id: 'card1', file: 'card1_hook.png' },
  { id: 'card2', file: 'card2_hire_cost.png' },
  { id: 'card3', file: 'card3_dps_cost.png' },
  { id: 'card4', file: 'card4_comparison.png' },
  { id: 'card5', file: 'card5_cta.png' },
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Viewport larger than any card so nothing clips
  await page.setViewportSize({ width: 1200, height: 1200 });

  const filePath = path.resolve(__dirname, 'carousel_hire_vs_dps.html');
  await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });

  for (const card of cards) {
    const el = await page.$(`#${card.id}`);
    await el.screenshot({
      path: path.join(OUTPUT_DIR, card.file),
      type: 'png',
    });
    console.log(`Saved: ${card.file}`);
  }

  await browser.close();
})();
