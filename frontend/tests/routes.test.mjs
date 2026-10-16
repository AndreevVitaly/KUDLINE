import assert from 'node:assert/strict'
import {readFileSync} from 'node:fs'

const main = readFileSync(new URL('../src/main.tsx', import.meta.url), 'utf8')
const header = readFileSync(new URL('../src/components/Header.tsx', import.meta.url), 'utf8')
const home = readFileSync(new URL('../src/pages/HomeOverviewPage.tsx', import.meta.url), 'utf8')

for (const route of ['/', '/about', '/services', '/production', '/projects', '/advantages', '/contacts', '/request']) {
  assert.match(main, new RegExp(`path=["']${route.replace('/', '\\/')}["']`), `Route ${route} is missing`)
}
for (const route of ['/about', '/services', '/production', '/projects', '/advantages', '/contacts', '/request']) {
  assert.ok(header.includes(route), `Header link ${route} is missing`)
}
assert.ok(home.includes('to="/request"'), 'Hero request CTA is missing')
assert.ok(home.includes('to="/projects"'), 'Hero projects CTA is missing')
assert.ok(main.includes('path="*"'), 'NotFound route is missing')
console.log('Frontend route, navigation and CTA checks passed')
