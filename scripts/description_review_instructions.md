# GRYNA STUDIO – product title & description review (Lithuanian)

GRYNA STUDIO is an online fashion store for women in Lithuania. All storefront text is
in **Lithuanian**. The product texts were machine-translated (mostly from German/English
supplier copy) and partly AI-written. Your job is to make every title and description
correct, natural, consistent Lithuanian that a native Lithuanian copy editor would approve.

You receive a JSON batch file: a list of products
`{id, title, productType, options: {"Spalva": [...], "Dydis": [...]}, html}`.
`options` are the product's REAL variant values (already corrected). `html` is the
description (already cleaned of junk attributes).

## 1. Title (`title`) – always return a title

Format: `<Name> | <descriptor>` – keep the first part (the person's name, e.g. "Lėja") exactly
as it is. Rewrite the descriptor so that it is:

- natural Lithuanian, **sentence case** (only the first word capitalised; no Title Case);
- **specific**: product noun + 1–2 concrete distinguishing features taken from the description
  or the options (pattern, fabric, cut, length, sleeve, neckline, heel, closure, print…),
  e.g. "Ilga gėlėta suknelė su V formos iškirpte", "Lininė palaidinė plačiomis rankovėmis",
  "Odinės basutės su pinta juostele". Avoid empty generic descriptors such as
  "Elegantiška vasarinė palaidinė" / "Patogi vasarinė suknelė" when the text gives you any
  concrete feature. Many products share generic descriptors today – make them distinct;
- 2–7 words, whole title ≤ 70 characters;
- no codes (e.g. "(P608)"), no repeated segments ("| Suknelė" at the end), no foreign words
  (Kühn, Used-Look, Vichy → languotas, etc.), no quotes unless it is a real print name;
- do not invent features that are not in the description/options/title.

If the product is "Arbatpinigiai" (a tip, not a fashion item) keep its title unchanged.

## 2. Description (`html`)

Fix, don't rewrite for the sake of it. Keep the structure, images (`<img>` tags exactly as they
are), tables, lists and the general length. Correct:

1. **Language**: grammar, cases, agreement, punctuation, unnatural machine-translated phrases,
   calques, wrong words. Any text in English/German/other languages → translate into Lithuanian.
   Headings (`<h2>/<h3>`) in sentence case. Lithuanian quotes „…“, en dash – , "%" written as "50 %".
2. **Foreign model / brand names** in the text (e.g. "Audrey megztinis", "Verity suknelė",
   "Delyziah", "SENNA", "Charm™", "Hailey", "Louisa", "Karin", "Marissa") → replace with the
   product's own name from the title ("Lėja suknelė", "megztinis Skaistė") or a neutral noun
   ("ši suknelė"). Never leave another brand's name.
3. **Other countries / fake origin claims**: remove claims like "Kanados prekės ženklas",
   "Įsikūrę Toronte", "Kodėl Kanados/vokiečių moterys mėgsta…" → neutral wording
   ("Kodėl jums patiks…"). Descriptions of a print (e.g. Eiffel tower print) may stay.
4. **Remove all return/refund/guarantee promises**: "100 % pasitenkinimo garantija",
   "lengvas grąžinimas", "pinigų grąžinimas", "nemokamas grąžinimas", "garantuojame…" etc.
   Returns are explained only in the store policy.
5. **Remove any delivery time / shipping speed statements** ("pristatymas per 3–5 dienas",
   "greitas pristatymas", "išsiunčiame per 24 val."). "Nemokamas pristatymas" may stay.
6. **Keep scarcity/urgency phrases** (e.g. "ribotas kiekis", "Kai kurių dydžių nebėra",
   "liko nedaug") – the owner wants them. Just correct their language.
7. **Facts must match the real options**: if the text lists available sizes or colours, make
   it match `options` exactly (e.g. "Galimi dydžiai nuo XS iki 5XL" when Dydis = S…2XL →
   "Galimi dydžiai: S–2XL"). Do not add size/colour lists that are not already there.
8. **No medical promises** for orthopedic shoes: "gydo", "pašalina skausmą", "išgydo" →
   softer wording ("padeda sumažinti spaudimą", "suteikia daugiau komforto").
9. Emojis: keep at most simple "✓" bullets; remove decorative emojis (👉🔥✨ etc.).
10. Do not invent new facts (materials, measurements, certifications). Do not add new sections.
11. Allowed tags only: p, h2, h3, h4, ul, ol, li, strong, em, br, table, thead, tbody, tr, th, td, img, a.
    Output must be valid HTML (all tags closed).

## 3. Output

Write ONE JSON file (path given in your task) containing an array with one object per input
product, in the same order:

```json
{"id": "gid://shopify/Product/…", "title": "Lėja | Lengva lininė suknelė be rankovių",
 "edits": [{"old": "exact substring of the input html", "new": "replacement"}],
 "html": null}
```

- Prefer `edits`: each `old` must be copied **exactly** from the input `html` (it must occur
  exactly once; make it long enough to be unique) and is applied in order. Use as many edits
  as needed to fix everything.
- If more than ~40 % of the text needs changes, set `"edits": []` and put the full corrected
  description in `"html"` instead.
- If the description needs no change: `"edits": [], "html": null`.
- Write valid JSON (escape quotes `\"` and newlines `\n` inside strings). After writing, run
  `python3 -c "import json;d=json.load(open('<your output file>'));print(len(d))"` to verify it
  parses and the count equals the number of input products; fix the file if not.

Work through every product carefully – read the whole description each time.
