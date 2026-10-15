"""Gera ficheiros de chamada (query + variables) para productUpdate em lote.

Uso: build_product_update_batches.py final_dir out_dir [max_por_chamada]
Cada ficheiro out_dir/uNNN.json = {"query": "...", "variables": {...}}.
Só inclui produtos com título ou descrição alterados.
"""
import json, sys, glob, os

def main(final_dir, out_dir, per=60, max_chars=120000):
    rows = []
    for f in sorted(glob.glob(os.path.join(final_dir, 'b*.json'))):
        for r in json.load(open(f)):
            if r['changedTitle'] or r['changedHtml']:
                inp = {'id': r['id']}
                if r['changedTitle']: inp['title'] = r['title']
                if r['changedHtml']: inp['descriptionHtml'] = r['descriptionHtml']
                rows.append(inp)
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(os.path.join(out_dir, 'u*.json')): os.remove(f)
    calls, cur, size = [], [], 0
    for r in rows:
        l = len(json.dumps(r, ensure_ascii=False))
        if cur and (len(cur) >= per or size + l > max_chars):
            calls.append(cur); cur, size = [], 0
        cur.append(r); size += l
    if cur: calls.append(cur)
    for k, c in enumerate(calls):
        decl = ','.join(f'$p{i}:ProductUpdateInput!' for i in range(len(c)))
        body = ' '.join(f'p{i}:productUpdate(product:$p{i}){{userErrors{{field message}}}}' for i in range(len(c)))
        q = f'mutation({decl}){{{body}}}'
        json.dump({'query': q, 'variables': {f'p{i}': r for i, r in enumerate(c)}},
                  open(os.path.join(out_dir, f'u{k:03d}.json'), 'w'), ensure_ascii=False)
    print('products', len(rows), 'calls', len(calls))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], *(int(a) for a in sys.argv[3:]))
