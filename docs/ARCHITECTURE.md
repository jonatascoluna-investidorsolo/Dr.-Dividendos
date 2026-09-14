# Arquitetura v0.1

## Princípios

1. Fonte e cálculo são separados.
2. Toda informação externa deve ter fonte, data de coleta e período de referência.
3. Reapresentações não devem apagar silenciosamente versões anteriores.
4. O motor deve ser determinístico: mesmos inputs + mesmos parâmetros = mesmo resultado.
5. Instituições financeiras têm regras próprias.
6. Parâmetros da metodologia são dados configuráveis, não constantes espalhadas no código.

## Próximos módulos

- `adapters/cvm.py`: DFP/ITR
- `adapters/b3.py`: eventos corporativos
- `adapters/market.py`: cotação
- `repositories/`: PostgreSQL
- `jobs/`: rotinas diárias/semanais
- `validation/`: reconciliação e alertas
- `api/`: endpoints públicos/admin

## Critério de produção

Nenhuma atualização automática deve ser liberada para assinantes antes de passar pela bateria de comparação com a planilha-base.
