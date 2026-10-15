# Cópia de segurança antes da limpeza para lituano (2026-10-15)

Estado do conteúdo da loja **antes** das alterações (lituano passou a ser o idioma principal).

- `collections-pages-menus.json` – 204 coleções (título, descrição, SEO, regras), 5 páginas, blog, menus (originais em português)
- `products-*.json` – 1368 produtos (título, descrição, tipo, SEO)
- `translatable-sample-incl-filters-blog.json` – amostra de textos traduzíveis (filtros, blog, envio)

## Alterações feitas
- Coleções (204): títulos, descrições e SEO passaram para lituano (handles inalterados).
- Páginas (5): Kontaktai, DUK, Apie mus, Užsakymo sekimas, Dydžių lentelė.
- Blog: "Notícias" -> "Naujienos". Envio: descrição do método em lituano.
- Produtos (14): títulos em alemão/inglês, 2 descrições em inglês/HTML colado, SEO em alemão.

- Tipos de produto (1368): 99 valores confusos (códigos "CL-0680", "Kelnaičių išpardavimas", "Women's clothing", etc.; 802 produtos sem tipo) -> 26 tipos em lituano. Mapa aplicado em `product-types-applied.jsonl`; regras em `scripts/classify_product_types.py` (os produtos antigos estão em `products-*.json`).
- Mais 5 títulos de calçado/calças mal traduzidos ("Smailioji pasaga" = "Absätze"...) corrigidos.

## Por fazer
- Filtros "Disponibilidade" e "Preço" (editar em Search & Discovery).
- Nome interno do perfil de envio "Perfil geral".
- Tema (4761 textos) e tradução para inglês.
