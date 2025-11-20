# Code References & Inspirations

All the clever tricks, patterns, and techniques used in Krawl's JavaScript, properly attributed.

## Pattern Index

| # | Technique | Module | Line(s) |
|---|-----------|--------|---------|
| [1] | Set ↔ Array Conversion | `storage.js` | 42, 52 |
| [2] | Ternary Default Pattern | `storage.js` | 52 |
| [3] | Unicode Star Symbols | `bookmarks.js` | 74 |
| [4] | classList.toggle() with State | `bookmarks.js` | 76 |
| [5] | DOM as Database | `bookmarks.js` | 87 |
| [6] | CSS Attribute Selectors | `bookmarks.js` | 93 |
| [7] | Optional Chaining (?.) | `bookmarks.js` | 98 |
| [8] | Haversine Formula | `map.js` | 135 |
| [9] | atan2() vs atan() | `map.js` | 149 |
| [10] | Pipeline Pattern | `filters.js` | 86 |
| [11] | Early Return / Guard Clauses | `filters.js` | 107 |
| [12] | for...of Loop | `filters.js` | 98 |
| [13] | Array.some() | `filters.js` | 104 |
| [14] | Optional Chaining + Nullish | `filters.js` | 121 |
| [15] | Spread for Set → Array | `events.js` | 179 |
| [16] | flatMap() | `events.js` | 180 |
| [17] | filter(Boolean) | `events.js` | 181 |
| [18] | Event Delegation | `main.js` | 140 |
| [19] | Element.matches() | `main.js` | 145 |
| [20] | mailto: Protocol | `main.js` | 359 |
| [21] | Debug API on window | `main.js` | 373 |

---

## Detailed References

### [1] Set ↔ Array Conversion Pattern
**Source:** MDN Web Docs - Set  
**URL:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set  
**Where:** `storage.js` lines 42, 52  
**Why:** Sets can't be JSON-serialized directly. `Array.from()` + `new Set()` provides clean conversion with O(1) lookups in memory vs O(n) for Array.includes().

---

### [2] Ternary Default Pattern
**Source:** JavaScript: The Good Parts (Douglas Crockford, 2008)  
**Where:** `storage.js` line 52  
**Why:** `data ? parse(data) : default` is more elegant than if/else for fallback values. Crockford's influence on modern JS best practices is massive.

---

### [3] Unicode Star Symbols
**Source:** Unicode Character Table  
**URL:** https://unicode-table.com/en/sets/star-symbols/  
**Where:** `bookmarks.js` line 74  
**Why:** ★ (U+2605) vs ☆ (U+2606) provide instant visual feedback without image assets or icon fonts. Zero dependencies.

---

### [4] classList.toggle() with State Parameter
**Source:** MDN Web Docs - Element.classList  
**URL:** https://developer.mozilla.org/en-US/docs/Web/API/Element/classList  
**Where:** `bookmarks.js` line 76  
**Why:** toggle() accepts a boolean second parameter to force add/remove. Avoids if/else boilerplate. Most developers don't know this!

---

### [5] DOM as Database Pattern
**Source:** Tom Dale (Ember.js) - "The Front-end Database"  
**URL:** https://tomdale.net/2015/02/youre-missing-the-point-of-server-side-rendered-javascript-apps/  
**Where:** `bookmarks.js` line 87  
**Why:** For static sites, HTML IS the data. Why duplicate event data in JS when it's already in the DOM? Scrape it. KISS over architectural purity.

---

### [6] CSS Attribute Selectors
**Source:** CSS Tricks - Attribute Selectors  
**URL:** https://css-tricks.com/almanac/selectors/a/attribute/  
**Where:** `bookmarks.js` line 93  
**Why:** `[data-foo="bar"]` is often faster than `.class` or `#id` for dynamic lookups. Great for data-driven UIs.

---

### [7] Optional Chaining Operator (?.)
**Source:** TC39 Proposal - Optional Chaining (ES2020)  
**URL:** https://github.com/tc39/proposal-optional-chaining  
**Where:** `bookmarks.js` line 98, `filters.js` line 121  
**Why:** Before this, defensive coding required `x && x.y && x.y.z`. Optional chaining collapsed entire patterns into elegant syntax. Game-changer for DOM safety.

---

### [8] Haversine Formula for Great-Circle Distance
**Source:** R.W. Sinnott, "Virtues of the Haversine" (Sky & Telescope, 1984)  
**Also:** Movable Type Scripts  
**URL:** https://www.movable-type.co.uk/scripts/latlong.html  
**Where:** `map.js` line 135  
**Why:** Gold standard for calculating distances on a sphere since 1984. Accounts for Earth's curvature. <0.5% error vs. Vincenty (which is way more complex).

---

### [9] atan2() vs atan()
**Source:** "Numerical Recipes" (Press et al., 1986)  
**Where:** `map.js` line 149  
**Why:** `atan2(y, x)` handles quadrants correctly, `atan(y/x)` doesn't. Knows signs of both arguments, determines correct quadrant. Old-school numeric wisdom.

---

### [10] Pipeline Pattern for Filtering
**Source:** Functional Programming (Haskell, Unix pipes)  
**Also:** "Eloquent JavaScript" by Marijn Haverbeke  
**URL:** https://eloquentjavascript.net/05_higher_order.html  
**Where:** `filters.js` line 86  
**Why:** Each filter is a stage. Event passes through or gets eliminated. Unix philosophy applied to data. Easier to debug than nested if/else trees.

---

### [11] Early Return / Guard Clauses
**Source:** "Refactoring" by Martin Fowler (1999)  
**URL:** https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html  
**Where:** `filters.js` line 107  
**Why:** `continue` is early return for loops. Reduces nesting, improves readability. Fowler's book revolutionized code structure thinking.

---

### [12] for...of Loop (ES6)
**Source:** TC39 ECMAScript 2015 Spec  
**URL:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of  
**Where:** `filters.js` line 98  
**Why:** Cleaner than `for (let i=0; i<len; i++)`. No index tracking. Off-by-one bugs impossible.

---

### [13] Array.some() for Existence Check
**Source:** Functional patterns, popularized by Underscore.js (2009)  
**URL:** https://underscorejs.org/#some  
**Where:** `filters.js` line 104  
**Why:** Stops iterating as soon as match found. O(n) worst case but often O(1). Jeremy Ashkenas made FP accessible to JS devs.

---

### [14] Optional Chaining + Nullish Coalescing
**Source:** TC39 Proposal - Optional Chaining (ES2020)  
**URL:** https://github.com/tc39/proposal-optional-chaining  
**Where:** `filters.js` line 121  
**Why:** `obj?.prop` returns undefined if obj is null/undefined. Replaces verbose `obj && obj.prop` checks. Massive DX improvement.

---

### [15] Spread Operator for Set → Array
**Source:** TC39 ECMAScript 2015 - Spread Syntax  
**URL:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax  
**Where:** `events.js` line 179  
**Why:** `[...new Set(array)]` is most elegant array deduplication. Alternative: `Array.from()` or manual loops. ES6 quality of life.

---

### [16] flatMap() for Nested Array Flattening
**Source:** TC39 ECMAScript 2019 (ES10)  
**URL:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flatMap  
**Where:** `events.js` line 180  
**Why:** `flatMap()` = `map()` + `flat()` in one pass. Before ES10: `array.map().flat()` or `reduce()`. More readable AND performant. Underrated ES10 feature.

---

### [17] filter(Boolean) for Truthy Values
**Source:** JavaScript idiom (jQuery era)  
**Where:** `events.js` line 181  
**Why:** Removes null, undefined, 0, "", false, NaN in one go. `Boolean` coerces to boolean. Passing it as callback = genius. More elegant than `.filter(x => x)`.

---

### [18] Event Delegation Pattern
**Source:** David Walsh (2012) + jQuery .on() (2006-2012)  
**URL:** https://davidwalsh.name/event-delegate  
**Where:** `main.js` line 140  
**Why:** One listener on parent vs. thousands on children. Works for dynamic elements. Memory-efficient. Fundamental DOM pattern pre-dating frameworks.

---

### [19] Element.matches() for Selector Checking
**Source:** DOM Living Standard  
**URL:** https://developer.mozilla.org/en-US/docs/Web/API/Element/matches  
**Where:** `main.js` line 145  
**Why:** Uses CSS selector syntax. Before this: manual `classList.contains()` or ID checks. Unified API for ANY selector. Elegant DX.

---

### [20] mailto: Protocol for Email Integration
**Source:** RFC 6068 - The 'mailto' URI Scheme (2010)  
**URL:** https://www.rfc-editor.org/rfc/rfc6068.html  
**Where:** `main.js` line 359  
**Why:** Zero dependencies for email. Browser opens default client. Works on mobile (Gmail/Mail/Outlook). Old-school web API that still works perfectly.

---

### [21] Debug API on window Object
**Source:** Chrome DevTools (2008+), jQuery ($), Lodash (_)  
**Where:** `main.js` line 373  
**Why:** Exposing modules on `window` makes REPL debugging effortless. Type `krawl.events.getStats()` in console. No breakpoints needed. This is how jQuery became so developer-friendly.

---

## Meta-Insights

### Most Influential Books/Resources
1. **"JavaScript: The Good Parts"** (Douglas Crockford, 2008) - Shaped modern JS best practices
2. **"Refactoring"** (Martin Fowler, 1999) - Code structure patterns
3. **"Eloquent JavaScript"** (Marijn Haverbeke) - Functional programming accessible
4. **MDN Web Docs** - The authoritative web API reference
5. **TC39 Proposals** - Bleeding edge JS features with rationale

### Most Impactful JavaScript Features
- **ES6 (2015):** for...of, spread, arrow functions, destructuring
- **ES2019:** flatMap
- **ES2020:** Optional chaining, nullish coalescing

### Clever vs. Clear
All techniques here prioritize **clarity** over cleverness, except where the "clever" solution is also simpler (e.g., `filter(Boolean)`). KISS principle trumps showing off.

---

*This document serves as both attribution and educational resource. Every trick has a story.*
