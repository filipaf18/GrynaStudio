"""Correções globais finais sobre desc_final/*.json -> desc_final2/*.json.

Remove afirmações de fornecedor não verificáveis, depoimentos copiados,
imagens vazias/alheias, converte tabelas em polegadas para cm.
"""
import json, glob, re, os, sys

SUBS = [
    (r'Kodėl šimtai moterų mėgsta šią (midi |maksi )?suknelę', lambda m: 'Kodėl jums patiks ši ' + (m.group(1) or '') + 'suknelė'),
    (r'Kodėl šimtai moterų (mėgsta|renkasi) (šį|šią|šiuos|šias) ([^<:]+?)(\s*[:<])', lambda m: 'Kodėl jums patiks ' + m.group(3) + m.group(4)),
    (r'atspindi dešimtmečių patirtį', 'atlikta kruopščiai'),
    (r'rankų darbo\s+', ''),
    (r'Kodėl[^<:]*šimtai moterų[^<:]*', 'Kodėl jums patiks'),
    (r'Jubiliejinis išpardavimas', 'Išpardavimas'),
    (r'<p>„[^<]{5,300}“\s*[–-]\s*Hélène M\., 61 m\.</p>\s*', ''),
    (r'<p>\s*<img/>\s*</p>\s*', ''), (r'<img/>', ''),
    (r'<p>\s*<img[^>]*Man_Boobs[^>]*>\s*</p>\s*', ''), (r'<img[^>]*Man_Boobs[^>]*>', ''),
]

def conv_inch_tables(h):
    """Converte para cm as tabelas que vêm depois de uma menção a polegadas
    ("coliais") e cujos valores são claramente polegadas (mediana < 60)."""
    i = h.find('coli')
    if i < 0: return h
    def conv_table(tm):
        tb = tm.group(0)
        nums = [float(x.replace(',', '.')) for x in re.findall(r'<td[^>]*>\s*(\d+(?:[.,]\d+)?)\s*</td>', tb)]
        if not nums or sorted(nums)[len(nums)//2] >= 60: return tb
        def cell(cm):
            num = re.fullmatch(r'\s*(\d+(?:[.,]\d+)?)\s*(?:[-–]\s*(\d+(?:[.,]\d+)?))?\s*', cm.group(2))
            if not num: return cm.group(0)
            f = lambda x: str(round(float(x.replace(',', '.')) * 2.54))
            return cm.group(1) + f(num.group(1)) + ('–' + f(num.group(2)) if num.group(2) else '') + cm.group(3)
        tb = re.sub(r'(<td[^>]*>)([^<]*)(</td>)', cell, tb)
        return re.sub(r'\(?\bcoli(ais|ai|ų)\)?', '(cm)', tb)
    head, tail = h[:i], h[i:]
    tail = re.sub(r'<table>.*?</table>', conv_table, tail, flags=re.S)
    tail = re.sub(r'\(coliais\)', '(cm)', tail)
    tail = re.sub(r'\bcoliais\b', 'cm', tail)
    return head + tail

def main(src='desc_final', dst='desc_final2'):
    os.makedirs(dst, exist_ok=True)
    changed = []
    for f in sorted(glob.glob(os.path.join(src, 'b*.json'))):
        R = json.load(open(f))
        for r in R:
            h0 = r['descriptionHtml']; h = h0
            for p, s in SUBS: h = re.sub(p, s, h)
            h = conv_inch_tables(h)
            if h != h0:
                r['descriptionHtml'] = h; r['changedHtml'] = True; changed.append(r['id'])
        json.dump(R, open(os.path.join(dst, os.path.basename(f)), 'w'), ensure_ascii=False, indent=1)
    print('postfix changed', len(changed))
    json.dump(changed, open(os.path.join(dst, '_postfix_changed.json'), 'w'))

if __name__ == '__main__':
    main(*sys.argv[1:])
