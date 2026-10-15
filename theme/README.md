# Tema — correções de lituano (2026-10-15)

O tema publicado ("GRYNA LT Launch v2 (Claude) — menu sem vazios") não pode ser editado por API.
As correções foram feitas numa cópia: **"GRYNA LT v3 — tema em lituano (rever e publicar)"**
(gid://shopify/OnlineStoreTheme/201799172479). Publicar no admin: Loja online → Temas.

Alterações na cópia:
- `locales/lt.json`: estava vazio (`{}`), por isso todos os textos da interface (Add to cart, carrinho,
  pesquisa, filtros, conta...) apareciam em inglês. Agora tem ~400 textos em lituano (cópia aqui).
- `templates/cart.json`: mensagem de envio grátis em inglês -> lituano.
- `templates/page.contact.json`: removidos campos de demonstração em inglês ("This is urgent", "Option one"...).
- `templates/page.faq.json`: removidos acordeões vazios de demonstração; ícones traduzidos.
- `templates/password.json`: "Coming Soon" -> "Netrukus atidarome".
- `templates/index.json`: erros de gramática corrigidos (secção "Apie mus", "Populiariausios prekės"),
  bloco "Drabužiai" passou a apontar para a coleção de roupa (antes apontava para calças).
- `sections/group-overlay.json` + `templates/cart.json`: mensagem do carrinho era o texto de exemplo do tema
  ("Use coupon code WELCOME10…", código que não existe) e o título "Cart" vinha do valor por defeito.
  Agora: título "Krepšelis" e mensagem sobre os descontos automáticos reais (-15% / -20% / -25%).
