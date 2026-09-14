# Quality Gate — v2.1

Objetivo: impedir que dados incompletos, inconsistentes ou sem rastreabilidade entrem no ranking principal.

## Estados
- APPROVED: identidade, período, fonte e indicadores críticos validados.
- REVIEW: existe dado utilizável, mas há pendência de validação/reconciliação.
- BLOCKED: identidade ou dado crítico não pode ser determinado com segurança.

## Regras mínimas
1. Ticker deve estar associado a emissor/CVM sem ambiguidade.
2. Cotação deve ter data, timestamp e provedor.
3. LPA/VPA devem carregar período de referência, data de coleta e fonte.
4. DPA deve derivar de eventos societários normalizados e ajustados.
5. Reapresentações não apagam versões anteriores; a versão vigente é selecionada pelo período + data de entrega.
6. Dívida líquida/EBITDA é `not_applicable` para instituições financeiras, nunca zero.
7. Qualquer conflito material entre fontes gera REVIEW, não substituição silenciosa.
8. Apenas APPROVED entra no ranking principal; REVIEW aparece separado e BLOCKED fica fora.
