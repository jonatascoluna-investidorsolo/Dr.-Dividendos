# Aquisição oficial — v2.6

A camada de aquisição agora trata DFP e ITR como artefatos auditáveis: URL, horário UTC, arquivo local, SHA-256 e estado da coleta.

Estados: `DOWNLOADED` ou `UNREACHABLE`.

Falha de rede nunca produz dado financeiro. O pipeline deve permanecer em `REVIEW` até que o arquivo oficial seja obtido e validado.

As URLs são as bases oficiais publicadas pela CVM. A B3 continua sendo a fonte preferencial para fechamento/market data contratado e eventos corporativos; o Yahoo permanece apenas como fallback técnico, nunca como fonte contábil.
