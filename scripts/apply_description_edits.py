"""Valida e aplica os resultados da revisão (desc_out/bNN.json) sobre as
descrições limpas (desc_batches/bNN.json).

Gera final/bNN.json com {id, title, descriptionHtml, changedTitle, changedHtml}
e lista problemas (edits que não aplicam, HTML inválido, imagens perdidas,
textos proibidos que ficaram).
"""
import json, re, sys, html as H
from html.parser import HTMLParser

FORBIDDEN = [r'pasitenkinimo garantij', r'pinigų grąžinim', r'lengv\w* grąžinim', r'nemokam\w* grąžinim',
             r'Kanados', r'Toront', r'\d+\s*[–-]\s*\d+\s*(darbo\s+)?dien', r'greit\w* pristatym']
VOID = {'br', 'img', 'hr'}

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.err = []
    def handle_starttag(self, t, a):
        if t not in VOID: self.stack.append(t)
    def handle_endtag(self, t):
        if t in VOID: return
        if not self.stack or self.stack[-1] != t:
            self.err.append(f'unexpected </{t}> (open: {self.stack[-3:]})')
            if t in self.stack:
                while self.stack and self.stack.pop() != t: pass
        else:
            self.stack.pop()

def check_html(h):
    c = Checker(); c.feed(h); c.close()
    if c.stack: c.err.append(f'unclosed {c.stack}')
    return c.err

def main(inp, out, final):
    I = json.load(open(inp)); O = json.load(open(out))
    byid = {o['id']: o for o in O}
    res, probs = [], []
    for it in I:
        o = byid.get(it['id'])
        if not o:
            probs.append((it['title'], 'missing in output')); continue
        h = it['html']
        if o.get('html'):
            h = o['html']
        else:
            for e in o.get('edits') or []:
                n = h.count(e['old'])
                if n != 1:
                    probs.append((it['title'], f'edit old occurs {n}x: {e["old"][:80]!r}')); continue
                h = h.replace(e['old'], e['new'])
        errs = check_html(h)
        if errs: probs.append((it['title'], 'html: ' + '; '.join(errs[:3])))
        if len(re.findall(r'<img', h)) != len(re.findall(r'<img', it['html'])):
            probs.append((it['title'], 'image count changed'))
        txt = H.unescape(re.sub(r'<[^>]+>', ' ', h))
        for f in FORBIDDEN:
            if re.search(f, txt, re.I): probs.append((it['title'], f'forbidden left: {f}'))
        t = (o.get('title') or it['title']).strip()
        if len(t) > 80 or ('|' not in t and it['title'] != 'Arbatpinigiai'):
            probs.append((it['title'], f'title suspicious: {t!r}'))
        res.append({'id': it['id'], 'title': t, 'descriptionHtml': h,
                    'changedTitle': t != it['title'], 'changedHtml': h != it['html'], 'oldTitle': it['title']})
    json.dump(res, open(final, 'w'), ensure_ascii=False, indent=1)
    print(f'{inp}: {len(res)} ok-ish, titles changed {sum(r["changedTitle"] for r in res)}, html changed {sum(r["changedHtml"] for r in res)}, problems {len(probs)}')
    for p in probs: print('  PROBLEM', p)

if __name__ == '__main__':
    main(*sys.argv[1:4])
