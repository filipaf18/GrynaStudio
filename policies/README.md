# Políticas da loja (Settings → Policies)

A API não tem permissão `write_legal_policies`, por isso estes textos têm de ser
colados à mão no admin: **Definições → Políticas**, em cada política clicar no
botão `<>` (mostrar HTML) do editor, apagar tudo e colar o conteúdo do ficheiro.

| Política | Lituano (texto principal) | Inglês (tradução) |
|---|---|---|
| Envio / Pristatymo politika | `shipping.lt.html` | `shipping.en.html` |
| Reembolso / Grąžinimo politika | `refund.lt.html` | `refund.en.html` |

- A política de envio atual tem o HTML "escapado" (aparece `<p>`, `<strong>`… como texto).
  Colar `shipping.lt.html` resolve.
- Prazos de entrega (1–3 + 8–12 dias úteis) só aparecem nestas políticas.
- A política de devoluções deixa explícito que o cliente organiza, paga e é
  responsável pela devolução para o armazém na Ásia (exceto artigos defeituosos).
- Depois de colar o texto lituano, as traduções inglesas são registadas via
  API (Translate & Adapt) com os ficheiros `*.en.html`.
