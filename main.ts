// "Kitten and Yarn" — ai-happy-01 entry (Node 22, standard library only).
// Copies the entry.png beside this file to the output directory so the
// judge sees exactly those bytes. The gate takes a whole PNG or JPEG of
// at most 1 MiB and 1024 by 1024 pixels.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
if (!existsSync(src)) {
  throw new Error('entry.png is missing next to main.ts');
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));
const { size } = statSync(join(outDir, 'entry.png'));
if (size > 1024 * 1024) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
console.log(`Wrote ${join(outDir, 'entry.png')} (${size} bytes)`);
