// Rasterize our own SVG artwork for GitHub repository social previews.
import { Resvg } from '@resvg/resvg-js';
import { readFile, writeFile } from 'node:fs/promises';
for (const name of ['profile', 'yapper', 'seesky', 'portfolio']) {
  const input = await readFile(`assets/social/${name}.svg`);
  const renderer = new Resvg(input, { fitTo: { mode: 'width', value: 1200 } });
  await writeFile(`assets/social/${name}.png`, renderer.render().asPng());
}
console.log('Four social previews rendered at 1200 pixels.');
