import json,re,collections
P=json.load(open('all_products.json'))
# apply the title fixes already pushed
RULES=[ # (type, regex on lowercased descriptor + handle + old type) ordered
('Papuošalų rinkiniai', r'papuošalų rinkinys|apyrankių rinkinys|karolių rinkinys|juvelyrinių|set-in|-set\b|armband-set'),
('Auskarai', r'auskar|ohrring|creolen|ohrstecker'),
('Vėriniai', r'vėrin|karoli|grandinė|grandinėl|kaklo papuoš|kette|halskette|pakabuk'),
('Apyrankės', r'apyrank|armband|\bbracelet'),
('Žiedai', r'žied|\bring\b|-ring-|ringe'),
('Akiniai nuo saulės', r'akin|sonnenbrille|sunglass'),
('Maudymosi kostiumėliai', r'maudymos|bikin|plaukim|tankin|badeanzug|paplūdimio kost'),
('Kombinezonai', r'kombinezon|jumpsuit|overall|latzhose'),
('Komplektai', r'komplekt|ansambl|rinkinys|ensemble|\bset\b|dviejų dalių|kostiumėl'),
('Sijonai', r'\bsijon|\brok\b|\brokas|\broko|\bskirt'),
('Šortai', r'šort|bermud|\bshorts\b'),
('Kelnės', r'kelnės|kelnių|kelnes|džinsai|tamprės|legging|\bhose\b|trousers|pants|jogger|džogeri'),
('Suknelės', r'suknel|kleid|dress|robe\b|tunika-suknel|tunika suknel|chalat'),
('Rankinės', r'rankin|krepš|kuprin|piniginė|piniginės|clutch|\bbag\b|tasche|shopper|rankinukas'),
('Aulinukai', r'aulin|ilgaauli|botin|\bbotas|\bbotai\b|kaubojiš|stiefel|\bboots?\b'),
('Sportbačiai', r'sportbat|sportiniai|sneaker|turnschuh|sportinis batelis'),
('Mokasinai', r'mokasin|loafer|mocassin'),
('Balerinos', r'balerin|sabrinas|ballerin'),
('Basutės', r'basut|sandal|šlepet|chinel|kapčiai'),
('Aukštakulniai', r'absatze|aukštakulni|kulniuk|kulnai|kulnų|kulnais|pumps|high heel|stiletto'),
('Švarkai', r'švark|blazer|sakko'),
('Striukės ir paltai', r'striuk|\bpalt|sobretud|\bjacke|jacket|\bmantel|\bcoat|bomber|parka|trenč|plaščius|flisin|gobtuvu striuk|apsiaustas'),
('Liemenės', r'liemen(ė|es|ių)|weste|\bvest\b'),
('Megztiniai ir kardiganai', r'megzt|kardigan|cardigan|strick|pullover|džemper|golf|aukštu kakl|aukšta apykakl|bluzon|sweater|knit|hoodie|gobtuvu(?!.*striuk)'),
('Palaidinės ir topai', r'viršus|viršutin|palaidin|bluse|blouse|marškin(?!ėl)|košulė|tunik|kimono'),
('Palaidinės ir topai', r'marškinėl|\btop|maikė|t-shirt|shirt|body\b|bodis|crop'),
('Kelnės', r'kelni'),
]
FALLBACK=('Ortopediniai batai', r'ortoped|mary jane|merė|meri džein|terapini|\bbatai\b|\bbateliai\b|\bbatelis\b|avalyn|batelis|bateliai')
PRE=[('Maudymosi kostiumėliai', r'tankin|maudymos|bikin'),('Suknelės', r'tunik\w*[- ]suknel|tipo suknel'),('Kombinezonai', r'kombinezon'),('Striukės ir paltai', r'marškinių striuk')]
def head(text):
    for name,rx in PRE:
        if re.search(rx,text): return name
    best=None
    for i,(name,rx) in enumerate(RULES):
        m=re.search(rx,text)
        if m and (best is None or m.start()<best[0]): best=(m.start(),name)
    if best: return best[1]
    if re.search(FALLBACK[1],text): return FALLBACK[0]
    return None
def classify(p):
    desc=p['title'].split('|',1)[-1].lower()
    ptype=(p['productType'] or '').lower()
    hand=p['handle'].replace('-',' ')
    for text,src in ((desc,'title'),(ptype,'type'),(hand,'handle')):
        r=head(text)
        if r: return r,src
    return None,None
if __name__=='__main__':
    c=collections.Counter(); un=[]; src=collections.Counter()
    for p in P:
        t,s=classify(p); c[t]+=1; src[s]+=1
        if t is None: un.append(p)
    for t,n in c.most_common(): print(n,t)
    print(src)
    for p in un: print(p['id'].split('/')[-1],p['title'],'|',p['productType'],'|',p['handle'])
