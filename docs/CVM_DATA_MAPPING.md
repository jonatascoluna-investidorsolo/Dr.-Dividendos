# CVM — plano de mapeamento de fundamentos

## Fontes
- DFP: demonstrações financeiras anuais.
- ITR: informações financeiras trimestrais.
- FCA: identificação cadastral e relação com valores mobiliários.
- Cadastro: identificação das companhias abertas.

## Regras
1. O ticker é uma chave operacional, não a identidade contábil da empresa.
2. A identidade primária deve usar o código CVM + documento + período.
3. DFP/ITR devem ser armazenados com versão/reapresentação.
4. Cada valor deve carregar período de referência, data de divulgação, fonte e status de validação.
5. O parser não deve depender de uma única posição de coluna: usar os nomes oficiais dos campos e o metadata da CVM.
6. O LPA usado pelo motor deve distinguir lucro atribuível aos acionistas da controladora e lucro consolidado quando aplicável.
7. VPA deve usar patrimônio atribuível aos acionistas ordinários dividido pela base de ações correspondente.
8. Dívida líquida/EBITDA só será calculada para entidades em que a métrica seja economicamente aplicável.
9. Para financeiras, o indicador deve ser marcado como `not_applicable` e não convertido em zero.
10. Reapresentações não apagam versões anteriores.

## Próxima implementação
- Extrair o metadata oficial da CVM para um catálogo local de campos.
- Mapear contas DRE/Balanço/DFC para um modelo canônico.
- Criar testes com pelo menos uma empresa operacional e uma financeira.
- Comparar os indicadores canônicos com a planilha-base antes de ativar atualização automática.

## v0.6 — modelo contábil canônico

A normalização deixou de somar linhas por nome de conta. O motor agora:

- restringe cada métrica à demonstração correta (DRE, BPA ou BPP);
- separa lucro líquido de lucro atribuível aos acionistas da controladora;
- calcula dívida financeira a partir de circulante + não circulante, evitando somar novamente a linha-pai;
- registra evidência da conta usada e flags de qualidade;
- mantém a lógica de fallback explícita quando o lucro atribuível não é encontrado.

Ainda é necessária uma validação com arquivos reais DFP/ITR antes de considerar os mapeamentos de contas como definitivos. O Portal de Dados Abertos da CVM informa que DFP e ITR incluem linhas fixas e não fixas e são atualizados semanalmente com reapresentações. 
