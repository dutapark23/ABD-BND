const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const filePath = path.resolve(__dirname, 'dps_recovery_strategy_2026.html');
  await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });

  await page.pdf({
    path: path.resolve(__dirname, 'dps_recovery_strategy_2026.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });

  await browser.close();
  console.log('PDF generated: dps_recovery_strategy_2026.pdf');
})();
