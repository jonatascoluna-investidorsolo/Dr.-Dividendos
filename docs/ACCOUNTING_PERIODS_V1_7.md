# v1.7 — Seleção de períodos contábeis e reapresentações

Esta camada define como o motor escolhe demonstrações anuais sem apagar o histórico.

## Regras

1. Cada combinação companhia + período de referência permanece no histórico.
2. Para um mesmo período, a versão mais recente/reapresentada vence para cálculo corrente.
3. Períodos anteriores continuam disponíveis para séries históricas e CAGR.
4. DFP é usado para o fechamento anual; ITR não substitui o DFP anual.
5. A camada de seleção não mistura períodos nem transforma ausência de dado em zero.
6. O cálculo LTM trimestral será tratado em camada própria, usando ITR e períodos comparáveis.

## Fonte oficial

A CVM informa que os conjuntos DFP e ITR são atualizados semanalmente com eventuais reapresentações. O DFP contém as demonstrações padronizadas e o ITR contém as informações trimestrais estruturadas. Portanto, versão, período de referência e data de divulgação são atributos obrigatórios para a seleção do dado.

## Próxima etapa

Implementar LTM/TTM para lucro e indicadores derivados, conciliando ITR trimestral, DFP anual e reapresentações, antes de usar esses valores no ranking de produção.
