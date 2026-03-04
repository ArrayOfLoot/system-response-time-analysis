# API SLA Performance Monitor

Este projeto simula e analisa o desempenho de uma API de um sistema acadêmico ao longo de um ano.

O objetivo é demonstrar como técnicas de análise estatística podem ser utilizadas para avaliar o tempo de resposta de sistemas e verificar se eles estão atendendo ao SLA (Service Level Agreement).

## Objetivo

Simular requisições de usuários ao sistema e analisar:

- tempo médio de resposta
- distribuição dos tempos de resposta
- percentual de requisições acima do SLA

O SLA definido para o sistema é de **500ms**.

## Metodologia

O processo de análise segue estas etapas:

1. Definição do problema  
   Verificar se o sistema acadêmico responde dentro do limite aceitável de desempenho.

2. Coleta de dados  
   Dados de requisições são simulados para representar o comportamento real do sistema.

3. Amostragem sistemática  
   Uma parte das requisições é selecionada para análise estatística.

4. Análise estatística  
   São calculados indicadores como média e percentual de requisições acima do SLA.

5. Visualização dos resultados  
   Histogramas mostram a distribuição dos tempos de resposta.

## Tecnologias utilizadas

- Python
- NumPy
- Plotly
- Pillow
- ImageIO

## Visualização

Para cada mês do ano é gerado um histograma mostrando a distribuição do tempo de resposta das requisições.

Esses gráficos são exportados como frames e combinados para gerar um vídeo mostrando a evolução do desempenho do sistema ao longo do tempo.

## Resultados

A análise permite identificar períodos em que o sistema sofre maior carga, como:

- matrícula
- semanas de prova
- fechamento de semestre

Durante esses períodos, o percentual de requisições acima do SLA tende a aumentar.

## Aplicação

Esse tipo de análise pode ser usado para:

- monitoramento de APIs
- análise de performance de sistemas
- identificação de gargalos
- planejamento de escalabilidade
