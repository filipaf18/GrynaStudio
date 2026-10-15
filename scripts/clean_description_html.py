"""Limpeza determinística do HTML das descrições (sem mexer no texto).

Remove restos de editores/ChatGPT (data-*, class, style, <meta>, <style>,
wrappers <div>/<span>), parágrafos vazios e espaços; mantém imagens,
tabelas, listas, títulos e links.
"""
import re
from bs4 import BeautifulSoup, Comment, NavigableString

KEEP_ATTRS = {'a': {'href'}, 'img': {'src', 'alt', 'width', 'height'}, 'td': {'colspan', 'rowspan'}, 'th': {'colspan', 'rowspan'}}
DROP_TAGS = ['style', 'script', 'meta', 'link', 'iframe', 'noscript', 'svg', 'button', 'input']
UNWRAP_TAGS = ['div', 'span', 'font', 'section', 'article', 'center', 'u', 'mark', 'small', 'big', 'form']
BLOCK = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'blockquote'}

def clean(html):
    soup = BeautifulSoup(html or '', 'html.parser')
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    for t in soup.find_all(DROP_TAGS):
        t.decompose()
    for t in soup.find_all(True):
        keep = KEEP_ATTRS.get(t.name, set())
        t.attrs = {k: v for k, v in t.attrs.items() if k in keep}
    for t in soup.find_all(UNWRAP_TAGS):
        t.unwrap()
    for t in soup.find_all(['b']):
        t.name = 'strong'
    for t in soup.find_all(['i']):
        t.name = 'em'
    for t in soup.find_all(['h1']):
        t.name = 'h2'
    # strong/em vazios ou aninhados
    for t in soup.find_all(['strong', 'em']):
        if not t.get_text(strip=True) and not t.find('img'):
            t.unwrap()
    for t in soup.find_all('strong'):
        if t.find_parent('strong'):
            t.unwrap()
    # títulos com <strong> dentro → só texto
    for h in soup.find_all(['h2', 'h3', 'h4']):
        for s in h.find_all('strong'):
            s.unwrap()
    # remover blocos vazios (sem texto e sem imagem)
    changed = True
    while changed:
        changed = False
        for t in soup.find_all(['p', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol', 'blockquote']):
            if not t.get_text(strip=True).replace('\xa0', '') and not t.find('img'):
                t.decompose(); changed = True
    out = str(soup)
    # imagens soltas (fora de <p>) ficam num parágrafo próprio
    out = re.sub(r'(?<!<p>)(<img [^>]+>)(?!</p>)', r'<p>\1</p>', out)
    out = out.replace('\xa0', ' ')
    out = re.sub(r'(<br\s*/?>\s*){2,}', '<br>', out)
    out = re.sub(r'<p>\s*<br\s*/?>', '<p>', out)
    out = re.sub(r'<br\s*/?>\s*</p>', '</p>', out)
    out = re.sub(r'[ \t]+', ' ', out)
    out = re.sub(r'\s*\n\s*', '\n', out)
    # quebras de linha só entre blocos
    out = re.sub(r'>\s+<', lambda m: '>\n<' if '\n' in m.group(0) else '> <', out)
    out = re.sub(r'\n+', '\n', out).strip()
    return out

if __name__ == '__main__':
    import json, sys
    P = json.load(open(sys.argv[1]))
    res = {x['id']: clean(x['descriptionHtml']) for x in P}
    json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False)
    before = sum(len(x['descriptionHtml'] or '') for x in P); after = sum(len(v) for v in res.values())
    print('chars before', before, 'after', after)
