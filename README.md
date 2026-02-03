# Teste Técnico – Estágio em Dados | IntuitiveCare

1. Visão geral
2. Arquitetura da solução
3. Pipeline de dados
4. Trade-offs técnicos
5. Como executar
6. Tratamento de inconsistências
7. Limitações e próximos passos

## Visão geral

Este projeto implementa um pipeline de dados para ingestão, processamento e consolidação das Demonstrações Contábeis de operadoras de planos de saúde publicadas pela ANS. O objetivo é extrair os dados dos três últimos trimestres disponíveis, identificar as despesas com eventos/sinistros e consolidá-las em um único arquivo estruturado para posterior validação, enriquecimento e análise.

## Arquitetura da solução

A solução foi estruturada em três camadas principais:

1. Ingestão de dados: responsável por localizar automaticamente os arquivos mais recentes da ANS, realizar o download dos arquivos ZIP e extrair seu conteúdo.
2. Processamento: leitura dos arquivos extraídos, identificação das contas relacionadas a despesas assistenciais (eventos e sinistros) e normalização dos dados.
3. Consolidação: geração de um arquivo CSV único contendo os dados de despesas consolidados por operadora e trimestre.

Essa arquitetura permite desacoplar a origem dos dados da lógica de transformação, facilitando manutenção e evolução futura.

## Pipeline de dados

1. O sistema acessa o repositório público da ANS em `/PDA/demonstracoes_contabeis/`.
2. Identifica automaticamente os arquivos ZIP dos três últimos trimestres disponíveis.
3. Realiza o download dos arquivos e os extrai para o diretório `data_extracted/`.
4. Cada arquivo CSV é lido individualmente e filtrado para manter apenas registros relacionados a despesas com eventos, sinistros ou contas assistenciais.
5. A data de cada registro é utilizada para inferir o ano e o trimestre.
6. Os registros são consolidados e enriquecidos com CNPJ e Razão Social a partir do cadastro oficial da ANS, gerando o arquivo final `consolidado_despesas_final.csv`.

## Trade-offs técnicos

### Processamento em memória vs incremental

Optou-se por um modelo de processamento incremental, no qual cada arquivo de demonstração contábil é lido e processado individualmente, em vez de carregar todos os arquivos simultaneamente em memória.

Essa decisão foi tomada considerando o volume potencialmente elevado de dados da ANS, que pode chegar a centenas de milhares de registros por trimestre. O processamento incremental reduz o consumo de memória, evita picos de uso de RAM e torna a solução mais robusta e escalável.

Como desvantagem, operações analíticas globais mais complexas exigiriam uma etapa posterior de agregação, porém para o objetivo de filtragem e consolidação de despesas este trade-off é aceitável e desejável.

## Como executar

1. Instale as dependências:
   python -m pip install requests pandas openpyxl

2. Execute o download e extração:
   python src/baixar_dados.py

3. Execute o processamento e consolidação:
   python src/processar_despesas.py

4. Execute o enriquecimento e consolidação final:
   python src/consolidar_final.py

5. O arquivo final será gerado como:
   consolidado_despesas_final.csv

## Tratamento de inconsistências

Durante a consolidação dos dados das demonstrações contábeis e do cadastro de operadoras da ANS, foram identificados os seguintes tipos de inconsistências:

1. CNPJs duplicados com razões sociais diferentes

O mesmo REG_ANS pode aparecer em diferentes arquivos trimestrais, porém a base oficial de cadastro (Relatorio_cadop.csv) foi utilizada como fonte única de verdade para CNPJ e RazaoSocial.
Dessa forma, quaisquer divergências de nomes nos arquivos contábeis foram ignoradas, garantindo padronização e confiabilidade.

2. Valores zerados ou negativos

Registros com ValorDespesas <= 0 foram removidos.
Esses valores normalmente representam ajustes contábeis, estornos ou correções, e não refletem despesas assistenciais reais. Mantê-los distorceria a análise financeira.

3. Datas e trimestres inconsistentes

Os arquivos contábeis utilizam a data da movimentação (DATA).
O trimestre foi inferido de forma programática a partir do mês da data, garantindo consistência entre diferentes arquivos e evitando depender de nomes ou estruturas externas.

4. Operadoras sem CNPJ válido

Registros sem correspondência no cadastro oficial (Relatorio_cadop.csv) foram descartados, pois não representam operadoras ativas ou válidas.

## Limitações e próximos passos

A consolidação final já integra os dados financeiros das demonstrações contábeis com o cadastro oficial de operadoras da ANS (Relatorio_cadop.csv), incluindo CNPJ e Razão Social.

Como próximos passos, o pipeline poderia ser estendido para:

- Validação de CNPJs junto à Receita Federal
- Análise de evolução temporal das despesas por operadora
- Implementação de testes automatizados de qualidade dos dados
- Armazenamento dos dados em banco relacional ou data warehouse
