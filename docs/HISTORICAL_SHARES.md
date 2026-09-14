# v0.9 — Histórico de ações e fundamentos

## Objetivo

Recalcular LPA/VPA históricos em uma base de ações comparável, evitando distorções causadas por splits, grupamentos e bonificações.

## Regra

Para um período histórico, o número de ações informado pela fonte é ajustado por eventos corporativos válidos posteriores ao fechamento do período e até a data de referência (`as_of`).

- split 2:1 → fator 2,0
- grupamento 1:2 → fator 0,5
- bonificação de 10% → fator 1,10

Eventos inválidos ou cancelados não entram no cálculo.

## Importante

Direitos de subscrição, conversões, incorporações, cisões e mudanças de classe não devem ser tratados como simples split. Devem possuir um adaptador específico quando a documentação da B3/CVM permitir determinar o fator econômico.

O sistema deve preservar o número originalmente reportado e o número ajustado; nunca sobrescrever o dado bruto.
