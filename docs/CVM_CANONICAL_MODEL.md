# Modelo contábil canônico — v0.7

O pipeline passa a separar três camadas:

1. **Raw CVM** — linhas originais das demonstrações.
2. **Normalização** — seleção das contas e agregação sem dupla contagem.
3. **Snapshot canônico** — conjunto auditável usado pelo motor financeiro.

## Regras principais

- Reapresentação: maior `VERSAO` vence para o mesmo período.
- Lucro: prioriza lucro atribuível quando disponível; mantém lucro líquido como evidência.
- Dívida: soma circulante + não circulante somente quando ambos são encontrados; caso contrário usa total explícito.
- Caixa: `Caixa e equivalentes de caixa`.
- Dívida líquida: dívida financeira - caixa.
- Dívida/EBITDA: calculada somente quando EBITDA > 0; a aplicação final ao score depende da classificação da empresa.
- Toda métrica mantém evidência da demonstração, código e descrição da conta.

## Limitação atual

A camada de contas ainda é uma primeira versão baseada em nomes + código quando disponível. Antes de produção, ela deve ser reconciliada contra os metadados oficiais da CVM e fixtures reais de DFP/ITR.

A CVM disponibiliza os arquivos DFP/ITR e seus metadados em arquivos ZIP estruturados e informa atualização semanal com reapresentações.
