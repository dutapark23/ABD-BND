const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

const docs = [
  { html: 'dps_recovery_strategy_2026.html',      pdf: 'dps_recovery_strategy_2026.pdf' },
  { html: 'dps_competitive_moat.html',             pdf: 'dps_competitive_moat.pdf' },
  { html: 'dps_studio_network_build_guide.html',   pdf: 'dps_studio_network_build_guide.pdf' },
  { html: 'dps_summer_meta_ads_2026.html',           pdf: 'dps_summer_meta_ads_2026.pdf' },
  { html: 'dps_october_market_share_strategy.html',  pdf: 'dps_october_market_share_strategy.pdf' },
  { html: 'dps_future_trends_rd_report_2026.html',  pdf: 'dps_future_trends_rd_report_2026.pdf' },
  { html: 'dps_spatial_audio_implementation.html', pdf: 'dps_spatial_audio_implementation.pdf' },
  { html: 'dps_video_studio_upgrade.html',         pdf: 'dps_video_studio_upgrade.pdf' },
];

(async () => {
  const browser = await chromium.launch();

  for (const doc of docs) {
    const page = await browser.newPage();
    const filePath = path.resolve(__dirname, doc.html);
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });
    await page.pdf({
      path: path.resolve(__dirname, doc.pdf),
      format: 'A4',
      printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
    });
    await page.close();
    console.log(`PDF generated: ${doc.pdf}`);
  }

  await browser.close();
})();
