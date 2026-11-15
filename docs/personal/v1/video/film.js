// node film.js <out.mp4> <w> <h> [site] [cta] [fps]  ->  films end-card.html frame by frame into an MP4
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
const fs = require('fs');
const [out, w = 1920, h = 1080, site = 'resume', cta = '', fps = 60] = process.argv.slice(2);
if (!fs.existsSync(path.resolve(__dirname, '../tokens.css'))) {
  console.error('tokens.css not found next to this folder. Run film.js from the published v1 folder (docs/personal/v1/video/ after a build, or a download of it).');
  process.exit(1);
}
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: +h } });
  const url = `file://${path.resolve(__dirname, 'end-card.html')}?film=1&w=${w}&h=${h}&site=${encodeURIComponent(site)}&cta=${encodeURIComponent(cta)}`;
  await p.goto(url); await p.evaluate(() => window.ready);
  const dur = await p.evaluate(() => DURATION); const n = Math.round(dur * fps);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) { await p.evaluate((t) => window.render(t), i / fps); ff.stdin.write(await p.screenshot({ type: 'png' })); }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r)); await b.close(); console.log(out, n, 'frames');
})();
