// Generate arcade artwork from public commit search, without personal tokens.
import { ArcadeRenderer } from 'pacman-contribution-graph';
import { mkdir, writeFile, rename } from 'node:fs/promises';
import { resolve } from 'node:path';

const output = resolve('assets/arcade');
const cache = new Map();
const nativeFetch = globalThis.fetch;
let fetchFailure;
let publicCommits = 0;
const cutoff = new Date();
cutoff.setUTCFullYear(cutoff.getUTCFullYear() - 1);
const since = cutoff.toISOString().slice(0, 10);

// The package's unauthenticated fetcher swallows API errors. Reject the build
// after simulation if any request failed, so old published images survive.
globalThis.fetch = async function (input) {
  try {
    const url = new URL(String(input));
    if (url.origin !== 'https://api.github.com' || url.pathname !== '/search/commits') {
      throw new Error('Unexpected arcade data source');
    }
    url.searchParams.set('q', `author:Xcape53 is:public committer-date:>=${since}`);
    const key = url.toString();
    if (!cache.has(key)) {
      const response = await nativeFetch(url, {
        headers: { Accept: 'application/vnd.github+json', 'User-Agent': 'Xcape53-profile' },
        signal: AbortSignal.timeout(25000)
      });
      if (!response.ok) throw new Error(`Public commit search returned ${response.status}`);
      const data = await response.json();
      if (!Array.isArray(data.items) || data.incomplete_results) throw new Error('Incomplete public commit search');
      if (data.total_count > 1000) throw new Error('Public search exceeds GitHub result limit');
      publicCommits = data.total_count;
      cache.set(key, JSON.stringify(data));
    }
    return new Response(cache.get(key), { headers: { 'Content-Type': 'application/json' } });
  } catch (error) {
    fetchFailure = error;
    throw error;
  }
};

try {
  const files = new Map();
  for (const game of ['galaga', 'breakout']) {
    for (const [theme, gameTheme] of [['dark', 'github-dark'], ['light', 'github']]) {
      let generated;
      await new ArcadeRenderer({
        game, platform: 'github', username: 'Xcape53', gameTheme,
        svgCallback: svg => { generated = svg; }
      }).start();
      if (fetchFailure) throw fetchFailure;
      if (!generated?.includes('<svg') || !generated.includes('<animate')) throw new Error('Arcade SVG is missing');
      // Keep the engineering palette. Embedded pixel art remains original.
      for (const [green, blue] of Object.entries({
        '#9be9a8':'#93c5fd', '#40c463':'#60a5fa', '#30a14e':'#8b5cf6', '#216e39':'#6d28d9',
        '#0e4429':'#183258', '#006d32':'#254c87', '#26a641':'#6366f1', '#39d353':'#a78bfa'
      })) generated = generated.replaceAll(green, blue);
      files.set(`${game}-${theme}.svg`, generated);
    }
  }
  await mkdir(output, { recursive: true });
  for (const [name, svg] of files) await writeFile(resolve(output, `${name}.tmp`), svg);
  for (const [name] of files) await rename(resolve(output, `${name}.tmp`), resolve(output, name));
  const counts = {};
  for (const page of cache.values()) {
    for (const record of JSON.parse(page).items) {
      const day = (record.commit.committer?.date ?? record.commit.author?.date)?.slice(0, 10);
      if (day) counts[day] = (counts[day] ?? 0) + 1;
    }
  }
  await mkdir(resolve('assets/data'), { recursive: true });
  await writeFile(resolve('assets/data/public-commits.json'), JSON.stringify({
    scope: 'publicly searchable commits', since, counts
  }, null, 2) + '\n');
  console.log(`Arcade generated from ${publicCommits} publicly searchable commits over the past year.`);
} catch {
  console.error('Arcade refresh failed; previously published SVGs are preserved.');
  process.exitCode = 1;
} finally {
  globalThis.fetch = nativeFetch;
}
