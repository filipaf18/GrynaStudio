"""Corrige os valores das opções (Spalva / Dydis / ...) dos produtos GRYNA.

Muitos valores vieram de traduções automáticas a partir do alemão
(Schwarz -> "Švarcas", Rot -> "Supuvęs" = "podre", Gelb -> "Help", ...).
Lê fresh/products.json (export Admin API) e gera option_updates.json com
as renomeações por produto/opção. Marcas de escassez como
"(beveik išparduota)" são mantidas (normalizadas em minúsculas).
"""
import json, re, sys
from collections import Counter

SUFFIX = re.compile(r'\s*\((beveik išparduota|išparduota|neturime sandėlyje|almost sold out)\)\s*$', re.I)
SUFFIX_NORM = {'beveik išparduota': '(beveik išparduota)', 'almost sold out': '(beveik išparduota)',
               'išparduota': '(išparduota)', 'neturime sandėlyje': '(neturime sandėlyje)'}

# ---- cores (spalva é feminino em lituano) ----
COLOR = {
 'Švarcas':'Juoda','Švarcas Švarcas':'Juoda','Juoda-juoda':'Juoda','Naktinė juoda':'Juoda','Onyx Juoda':'Juoda',
 'Safyro juoda':'Juoda','Venecija Juoda':'Juoda','Helė Švarc':'Juoda','Šviesiai juoda':'Juoda',
 'Braun':'Ruda','Grau':'Pilka','Pilka spalva':'Pilka','Pilkas':'Pilka','Žvaigždinis Grau':'Pilka',
 'Supuvęs':'Raudona','Toledu Rotas':'Raudona','Toledo Rot':'Raudona',
 'Help':'Geltona','Gelb':'Geltona','Gelis':'Geltona','Geltonas':'Geltona',
 'Rožė':'Rožinė','Rosa':'Rožinė','Lila':'Alyvinė','Alyvos':'Alyvinė',
 'Himmelblau':'Žydra','Žydras':'Žydra','Žydrasis':'Žydra',
 'Kremas':'Kreminė','Turkis':'Turkio spalvos','Turkio':'Turkio spalvos',
 'Abrikosas':'Abrikosinė','Leopardas':'Leopardo raštas','Kava':'Kavos spalvos','Kavos spalva':'Kavos spalvos','Coffee':'Kavos spalvos',
 'Tamsiai rudas':'Tamsiai ruda','Šviesiai rudas':'Šviesiai ruda','Sidabras':'Sidabrinė','Šviesiai pilkas':'Šviesiai pilka',
 'Šv.pilkas':'Šviesiai pilka','Šv.rožinė':'Šviesiai rožinė',
 'Smėlio spalva':'Smėlio spalvos','Smėlio':'Smėlio spalvos','Smėlio-Smėlinė':'Smėlio spalvos',
 'Baliska smėlio spalva':'Smėlio spalvos','Balio smėlio spalva':'Smėlio spalvos',
 'Auksinės spalvos':'Auksinė','Auksinis':'Auksinė','Auksaspalvis':'Auksinė','Aukso spalvos':'Auksinė',
 'Sidabro spalvos':'Sidabrinė','Sidabrinės spalvos':'Sidabrinė','Sidabrinė spalva':'Sidabrinė',
 'Violeta':'Violetinė','Violett':'Violetinė','Juoda Pilka':'Juoda-pilka','Juoda pilka':'Juoda-pilka','Juodai pilkas':'Juoda-pilka',
 'Juodas pilkas':'Juoda-pilka','Šampanas':'Šampano spalvos','Įvairiaspalvis':'Įvairiaspalvė',
 'Daugiaspalvis':'Daugiaspalvė','Daugiaspalvis 1':'Daugiaspalvė 1','Daugiaspalvis 2':'Daugiaspalvė 2',
 'Kupranugaris':'Kupranugario spalvos','Camel':'Kupranugario spalvos',
 'Juoda Mėlyna':'Juoda-mėlyna','Mėtų':'Mėtų žalia','Mėtų žalumo':'Mėtų žalia','Minzgrün':'Mėtų žalia',
 'Rožinio aukso spalvos':'Rožinio aukso','Rožinis auksas':'Rožinio aukso',
 'Stilius 1':'Modelis 1','Stil 2':'Modelis 2','Stilius 2':'Modelis 2','3 stilius':'Modelis 3','Stilius 3':'Modelis 3',
 '4 stilius':'Modelis 4','Stilius 5':'Modelis 5',
 'Rožė Violeta':'Rožinė-violetinė','Juoda/Balta':'Juoda-balta','Balta-juoda':'Balta-juoda','Terra Braun':'Terakotos ruda',
 'Raudonai rudas':'Raudonai ruda','Jūrų':'Jūrinė mėlyna','Vėžlio kiautas':'Vėžlio kiauto raštas','Vėžlys':'Vėžlio kiauto raštas',
 'Šarvuotoji strėliukė':'Vėžlio kiauto raštas','Šelpkartūnis':'Vėžlio kiauto raštas',
 'Pilkas leopardas':'Pilkas leopardo raštas','Juoda geltona':'Juoda-geltona','Auksinė / Juoda':'Auksinė / juoda',
 'Dramblio kaulo':'Dramblio kaulo spalvos','Dramblio Kaulas':'Dramblio kaulo spalvos','Dramblio Kaulo':'Dramblio kaulo spalvos',
 'Kakavos':'Kakavos spalvos','Pistacijų':'Pistacijų spalvos','Tabako':'Tabako spalvos','Koralo':'Koralų spalvos','Koralas':'Koralų spalvos',
 'Persiko':'Persikų spalvos','Persikas':'Persikų spalvos','Pelenų rožė':'Pelenų rožinė','Sena rožinė':'Senoji rožinė',
 'Taupe':'Pilkai ruda','Melionraudona':'Melionų raudona','Karališka mėlyna':'Karališkoji mėlyna','Karališko mėlynumo':'Karališkoji mėlyna',
 'Okeris':'Ochros spalvos','Ockeris':'Ochros spalvos','Vandenyno mėlynumo gėlės':'Mėlynos gėlės',
 'Gelsvai melsvas':'Gelsvai melsva','Rot-Rosa':'Raudonai rožinė','Rot Rosa':'Raudonai rožinė','Rosa Rot':'Raudonai rožinė',
 'Rotrosa':'Raudonai rožinė','Rožė Rot':'Raudonai rožinė','Rosenrot':'Rožių raudona','Smėlio/Rusvas':'Smėlio / rusva',
 'Buntas':'Margaspalvė','Karmazinas':'Karmino raudona','Marin Blau':'Jūrinė mėlyna','Levandų':'Levandų spalvos','Labas':'Levandų spalvos',
 'Dulkėti alyviniai žiedai':'Alyvinė su gėlėmis','Rosa Weiß':'Rožinė-balta','Žalia-Raudona':'Žalia-raudona','Aqua Blau':'Akvamarino',
 'White 2':'Balta 2','White':'Balta','Karamelinis rudas':'Karamelinė ruda','Vaivorykštė':'Vaivorykštės spalvų','Blue flowers':'Mėlynos gėlės',
 'Dark Flowers':'Tamsios gėlės','Gėlių galia':'Gėlių raštas 1','Gėlių galia 2':'Gėlių raštas 2',
 'Pavyzdys 1':'Raštas 1','Pavyzdys 2':'Raštas 2','3 pavyzdys':'Raštas 3','Pavyzdys 4':'Raštas 4','Pavyzdys 5':'Raštas 5',
 'Rožinis pilkumas':'Rausvai pilka','Geltona violetinė':'Geltona-violetinė','Chaki ir Balta':'Chaki ir balta',
 'Juoda / Smėlio':'Juoda / smėlio spalvos','Mėlynas povas':'Povo mėlyna','Graži gėlė':'Gėlių raštas','Exotic Black':'Juoda su raštu',
 'Žydroji gėlė':'Žydra su gėlėmis','Gryna Balta':'Balta','Alyvuogė':'Alyvuogių žalia','Alyvuogių':'Alyvuogių žalia',
 'Kobalto Mėlis':'Kobalto mėlyna','Mahogany ruda':'Raudonmedžio ruda','Atėnė Veis':'Balta','Atėnų balta':'Balta',
 'Grafitinė juoda':'Grafito juoda','Amazonės žaliasis':'Amazonės žalia','Balta Ruda':'Balta-ruda','Blau Weiß':'Mėlyna-balta',
 'Saulėgrąžų geltonumo':'Saulėgrąžų geltona','Mėlyna Balta':'Mėlyna-balta','Mėlyna-Balta':'Mėlyna-balta','Juoda balta':'Juoda-balta',
 'Bronza':'Bronzinė','Žydrasis vandenynas':'Vandenyno žydra','Kreminės baltumo':'Kreminė balta','Kreminės baltos spalvos':'Kreminė balta',
 'Gebrochenes Weiß':'Kreminė balta','Nešvari balta spalva':'Natūrali balta','Anglis':'Anglies pilka','Karamelė':'Karamelinė','Caramel':'Karamelinė',
 'Juoda gyvatė':'Juodas gyvatės raštas','Raudona gyvatė':'Raudonas gyvatės raštas','Žalioji gyvatė':'Žalias gyvatės raštas',
 'Juodieji abrikosai':'Juoda-abrikosinė','Tamsus abrikosas':'Tamsiai abrikosinė','Šviesus abrikosas':'Šviesiai abrikosinė',
 'Juodasis leopardas':'Juodas leopardo raštas','Smėlio spalvos leopardas':'Smėlio spalvos leopardo raštas',
 'Rudos spalvos leopardo raštas':'Rudas leopardo raštas','Leopardų rudumas':'Rudas leopardo raštas',
 'Šarlachas':'Skaisčiai raudona','Golvėjaus žalia':'Tamsiai žalia','Šteinas':'Slyvinė','Šviesiai auksinis kaštonas':'Šviesiai kaštoninė',
 'Oranžinė Rožinė Juoda':'Oranžinė-rožinė-juoda','Su spauda':'Su raštu','Juodas (dryžuotas)':'Juoda (dryžuota)',
 'Žalias (dryžuotas)':'Žalia (dryžuota)','Garstyčios':'Garstyčių spalvos','Fluorescent Green':'Neoninė žalia',
 'Odos spalva':'Kūno spalvos','Burgundas':'Bordo','Dryžuotas':'Dryžuota','Žalias':'Žalia','Konjakas':'Konjako spalvos',
 'Suede':'Zomšinė','Avižos':'Avižų spalvos','Kaštonas':'Kaštoninė','Samaninė žalia':'Samanų žalia',
 'Tamsiai mėlynas gobtuvas':'Tamsiai mėlyna su gobtuvu','Turkio spalvos gobtuvas':'Turkio spalvos su gobtuvu',
 'Juoda gobtuvas':'Juoda su gobtuvu','Violetinė kepurė su gobtuvu':'Violetinė su gobtuvu','Rožinis gobtuvas':'Rožinė su gobtuvu',
 'Raudonas gaubtas':'Raudona su gobtuvu','Burgundiškas gobtuvas':'Bordo su gobtuvu','Chaki gobtuvas':'Chaki su gobtuvu',
 'Mėlynas gobtuvas':'Mėlyna su gobtuvu','Turkio spalvos apykaklė':'Turkio spalvos su stačia apykakle',
 'Stovintysis kaklas tamsiai mėlynas':'Tamsiai mėlyna su stačia apykakle','Stovimoji apykaklė, juoda':'Juoda su stačia apykakle',
 'Violetinis stovas':'Violetinė su stačia apykakle','Bordo spalvos stovinčia apykakle':'Bordo su stačia apykakle',
 'Aukšta apykaklė, chaki':'Chaki su stačia apykakle','Stovio apykaklė raudona':'Raudona su stačia apykakle',
 'Chaki karinė žalia':'Chaki','Weiss Schwarz':'Balta-juoda','Violetinės juostelės':'Violetiniai dryžiai',
 'Rudai dryžuotas':'Rudi dryžiai','Juodos juostos':'Juodi dryžiai','Raudonos juostelės':'Raudoni dryžiai','Žalios juostos':'Žali dryžiai',
 'Smėlio Oranžinė':'Smėlio-oranžinė','Smėlio spalvos gėlės':'Smėlio spalvos su gėlėmis','Blumenblau':'Rugiagėlių mėlyna',
 'Akmeninis pilkšvai žalias':'Akmens žalia','Karamelinė smėlio spalva':'Karamelinė smėlio','Grafitas':'Grafito pilka',
 'Plytų raudonumo':'Plytų raudona','Žydra, dangaus mėlyna':'Dangaus žydra','Žydras dangaus mėlis':'Dangaus žydra',
 'Auksinės rudos spalvos':'Auksinė ruda','Aukso ruda':'Auksinė ruda','Vandens žalios spalvos':'Vandens žalia','Vaisinė žaluma':'Obuolių žalia',
 'Rožė-Švarcas':'Rožinė-juoda','Rosa – Schwarz':'Rožinė-juoda','Žalia-Juoda':'Žalia-juoda','Balai':'Juoda-balta dryžuota',
 'Atogrąžų':'Atogrąžų raštas','Taškai':'Taškuota','Punktai':'Taškuota','Juoda Ruda':'Juoda-ruda','Mėlyna Žalia':'Mėlyna-žalia',
 'Mėlyna - Žalia':'Mėlyna-žalia','Lašiša':'Lašišų spalvos','Tigerdruck':'Tigro raštas','Juodai-raudonas':'Juoda-raudona',
 'Žaliai balti':'Žalia-balta','Kamufliažas':'Kamufliažinė','Miškas':'Miško žalia','Dryžuota juoda':'Juoda dryžuota',
 'Jūrinės juostos':'Jūriniai dryžiai','Švarc Oranžas':'Juoda-oranžinė','Gyvūnų raštai':'Gyvūno raštas','Lila Gold':'Alyvinė-auksinė',
 'Pilka Balta':'Pilka-balta','Mėlynai geltonas':'Mėlyna-geltona','Rosablau':'Rožinė-žydra','Juoda Sidabrinė':'Juoda-sidabrinė',
 'Švarc (juoda) Dopl (dvi) Grau (pilka)':'Juoda, pilkas gradientas','Gold Doppel Grau':'Auksinė, pilkas gradientas',
 'Mėlyna Rožinė':'Mėlyna-rožinė','Mėlyna-Rožinė':'Mėlyna-rožinė','Raudonasis leopardas':'Raudonas leopardo raštas',
 'Leopardinis šampanas':'Leopardo raštas, šampano spalvos','Ruda Mėlyna':'Ruda-mėlyna','Pilka rožinė':'Pilka-rožinė',
 'Leoparden Grau':'Leopardo raštas, pilki stiklai','Švarcas Skaidrus':'Juoda-skaidri','Švarcas Braunas':'Juoda-ruda','Ruda Geltona':'Ruda-geltona',
 'Oranžinis leopardas':'Oranžinis leopardo raštas','Juoda žalia':'Juoda-žalia','Pilkas gradientas':'Pilka, gradientas','Skaidrus':'Skaidri',
 'Rožinis gradientas':'Rožinė, gradientas','Brauno gradientas':'Ruda, gradientas','Alyvinis gradientas':'Alyvinė, gradientas',
 'Baltos ir rausvos spalvų perėjimas':'Balta-rožinė, gradientas','Rožė-Rožė. Eiga':'Rožinė, rožinis gradientas',
 'Raudonai juodas':'Raudona-juoda','Poliarizuotas Juodas':'Juoda, poliarizuoti stiklai',
 'Polarizuoti leopardo raštai':'Leopardo raštas, poliarizuoti stiklai','Leopardų arbata':'Leopardo raštas, rudi stiklai',
 'Leopardo arbata':'Leopardo raštas, rudi stiklai','Tyti-Tyti':'Ruda, rudi stiklai','Tee Tee':'Ruda, rudi stiklai',
 'Marškinėliai su leopardo raštu':'Leopardo raštas, rudi stiklai','Leopardiniai marškinėliai':'Leopardo raštas, rudi stiklai',
 'Marškinėliai':'Ruda, rudi stiklai','Rosa Pantera':'Rožinė pantera','Okeano prospektas':'Ocean Drive','Auksas/Pilka':'Auksinė / pilka',
 'Auksinė/ruda':'Auksinė / ruda','Sidabrinė/Pilka':'Sidabrinė / pilka','Auksas/Žalia':'Auksinė / žalia','Auksas-Juoda':'Auksinė-juoda',
 'Aukso-žalios':'Auksinė-žalia','Skaidrus leopardas':'Skaidrus leopardo raštas','Rožinis Leopardas':'Rožinis leopardo raštas',
 'Auksinis rėmelis | Žali stiklai':'Auksinis rėmelis, žali stiklai','Auksinis rėmelis | Rudos spalvos lęšiai':'Auksinis rėmelis, rudi stiklai',
 'Sidabrinis rėmelis | Tamsinti stiklai':'Sidabrinis rėmelis, tamsinti stiklai','Juodi rėmeliai | Tamsinti stiklai':'Juodas rėmelis, tamsinti stiklai',
 'Auksinis rėmelis | Tamsinti stiklai':'Auksinis rėmelis, tamsinti stiklai','Vėžlio kiauto / Žalia':'Vėžlio kiauto raštas / žalia',
 'Juoda / Oranžinė':'Juoda / oranžinė','Vėžlio kiauto raštas / Oranžinė':'Vėžlio kiauto raštas / oranžinė','Juoda ir Balta':'Juoda ir balta',
 'Botaninis':'Botaninis raštas','Kelly Grün':'Smaragdo žalia','Mėlynas akvarelinis':'Mėlynas akvarelės raštas',
 'Žiedų puvinys':'Raudona su gėlėmis','Gėlių geltona':'Geltona su gėlėmis','Gėlių šviesiai mėlyna':'Šviesiai mėlyna su gėlėmis',
 'Gėlėtas mėlynas':'Mėlyna su gėlėmis','Gėlių':'Gėlių raštas 1','Gėlės':'Gėlių raštas 2','Gėlėtas motyvas':'Gėlių raštas',
 'Rostrotas':'Rūdžių raudona','Trišakis':'Rožinė-ruda','Dydis':'Juoda su raštu','Juodas':'Juoda',
 # akiniai: "rėmelis + stiklai" (vokiška "Tee" = arbatos spalvos, t. y. rudi stiklai)
 'Violett Violett':'Violetinė, violetiniai stiklai','Mėlyna mėlyna':'Mėlyna, mėlyni stiklai','Rožė Raudona':'Rožinė, raudoni stiklai',
 'Gelbė Gelbė':'Geltona, geltoni stiklai','Raudona Pilka':'Raudona, pilki stiklai','Pilka Raudona':'Pilka, raudoni stiklai',
 'Žalioji arbata':'Žalia, rudi stiklai','Rožinė arbata':'Rožinė, rudi stiklai','Apelsinų arbata':'Oranžinė, rudi stiklai',
 'Mėlynoji arbata':'Mėlyna, rudi stiklai','Pilkoji rožė':'Pilka, rožiniai stiklai','Pilka balta':'Pilka-balta',
 'Violetinė arbata':'Violetinė, rudi stiklai','Grüner Grün':'Žalia, žali stiklai','Švarcas Goldas':'Juoda-auksinė',
 'Žalia Auksas':'Žalia-auksinė','Šampaninis auksas':'Šampano auksinė','Rožinio aukso gradientas':'Rožinio aukso, gradientas',
 'Perėjimų marškinėliai „Gold“':'Auksinė, rudas gradientas','Sidabras Sidabras':'Sidabrinė','Lila Rosa':'Alyvinė-rožinė',
 'Auksinė arbata':'Auksinė, rudi stiklai',
 'Raudona/Mėlyna':'Raudona / mėlyna','Mėlyna-raudona':'Mėlyna-raudona','Juoda ir rožinė':'Juoda ir rožinė',
 '<div>Tamsiai žalia</div><div><br></div>':'Tamsiai žalia','Help Help':'Geltona',
}
PRINT = re.compile(r'^(?:(\d+)\s*(?:spaudinys|iš 9|trauka)|(?:Spausdinti|Spausdinimas|Spausdinimo|Spaudimas|Spauda|spauda|Spaudinys|Slėgis|Druck|Druckas)\s*(\d+)|(\d+) spaudinys)$')
PRINT_WORDS = {'Šeši spaudos darbai': 6}

SIZE = {
 'Universalus dydis':'Vienas dydis','Vienas dydis tinka visiems':'Vienas dydis','Normalus':'Vienas dydis','Reguliariai':'Vienas dydis',
 'Vieno dydžio(ilgis 62cm,kr.apimčiai iki 120cm)':'Vienas dydis (ilgis 62 cm, krūtinės apimtis iki 120 cm)',
 'EU36 (S)':'ES 36 (S)','ES38 (M)':'ES 38 (M)','ES40/42 (L)':'ES 40/42 (L)','ES44 (XL)':'ES 44 (XL)','ES46 (2XL)':'ES 46 (2XL)','EU48 (3XL)':'ES 48 (3XL)',
 'S (50-60 kg)':'S (50–60 kg)','M (60-70 kg)':'M (60–70 kg)','L (70-78 kg)':'L (70–78 kg)','XL (78-85 kg)':'XL (78–85 kg)',
 '2XL (85-95kg)':'2XL (85–95 kg)','3XL (95-105 kg)':'3XL (95–105 kg)','4XL (105-115 kg)':'4XL (105–115 kg)','5XL (115–125 kg)':'5XL (115–125 kg)',
 '6XL (125-135 kg)':'6XL (125–135 kg)','XXL':'2XL',
}
OTHER = {'52%viskozė 26%poliesteris 22%poliamidas':'52 % viskozė, 26 % poliesteris, 22 % poliamidas','Standartas':'Default Title'}

def fix_color(v):
    m = SUFFIX.search(v); suf = ''
    if m:
        suf = ' ' + SUFFIX_NORM[m.group(1).lower()]; v = v[:m.start()]
    v = v.strip()
    # tamanhos de malas dentro da cor: "Braun(31x27cm)" -> "Ruda (31x27 cm)"
    dim = re.match(r'^(.*?)\s*\((\d+)\s*x\s*(\d+)\s*cm\)$', v)
    if dim:
        return fix_color(dim.group(1)) + f' ({dim.group(2)}x{dim.group(3)} cm)' + suf
    num = re.match(r'^(Balta) (\d)$', v)
    if v in COLOR: v = COLOR[v]
    elif v in PRINT_WORDS: v = f'Raštas {PRINT_WORDS[v]}'
    else:
        p = PRINT.match(v)
        if p: v = 'Raštas ' + next(g for g in p.groups() if g)
    return v + suf

def fix_size(v):
    m = SUFFIX.search(v); suf = ''
    if m:
        suf = ' ' + SUFFIX_NORM[m.group(1).lower()]; v = v[:m.start()]
    v = v.strip()
    v = SIZE.get(v, v)
    es = re.match(r'^(\d+(?:\.\d)?) ES$', v)
    if es: v = es.group(1)
    return v + suf

# correções por produto (verificadas pelas fotos das variantes)
PRODUCT_OVERRIDES = {
 # calças: "Grau" é cinzento escuro e "Pilka spalva" é cinzento-acastanhado
 'gid://shopify/Product/15861843526015': {'Grau': 'Tamsiai pilka', 'Pilka spalva': 'Pilkai ruda'},
 'gid://shopify/Product/15861844050303': {'Grau': 'Tamsiai pilka', 'Pilka spalva': 'Pilkai ruda'},
 'gid://shopify/Product/15861847228799': {'Grau': 'Tamsiai pilka', 'Pilka spalva': 'Pilkai ruda'},
}

def main(src, out):
    P = json.load(open(src))
    updates, problems = [], []
    for x in P:
        for o in x['options']:
            f = {'Spalva': fix_color, 'Dydis': fix_size}.get(o['name'], lambda v: OTHER.get(v, v))
            ov = PRODUCT_OVERRIDES.get(x['id'], {})
            new = [(v['id'], v['name'], ov.get(v['name']) or f(v['name'])) for v in o['optionValues']]
            names = Counter(n for _, _, n in new)
            dup = [n for n, c in names.items() if c > 1]
            if dup:
                problems.append((x['title'], o['name'], dup, [(a, b) for _, a, b in new]))
                continue
            ch = [{'id': i, 'old': a, 'name': b} for i, a, b in new if a != b]
            if ch:
                updates.append({'product': x['id'], 'title': x['title'], 'option': o['id'], 'optionName': o['name'], 'values': ch})
    json.dump(updates, open(out, 'w'), ensure_ascii=False, indent=1)
    print('options to update:', len(updates), 'values:', sum(len(u['values']) for u in updates))
    for p in problems: print('DUP', p)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
