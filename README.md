# TC1 — Rede Neural para Previsão de Churn (End-to-End)

Descrição do repositório e do Tech Challenge

> INSERIR AQUI O DESCRITIVO DO TECH CHALLENGE (anexo). Por favor, cole ou anexe o enunciado para que eu incorpore o texto completo nesta seção.

## Resumo

Pipeline end-to-end para previsão de churn em operadora de telecomunicações. Inclui preparação de dados, modelagem (MLP em PyTorch), baselines com Scikit-learn, rastreamento de experimentos com MLflow, API com FastAPI e instruções para deploy em nuvem.

## Objetivo

Implementar um pipeline reprodutível para prever churn de clientes, acompanhar experimentos, comparar modelos e expor um endpoint para inferência em produção.

## Estrutura do repositório

- `data/` — dados brutos e processados
- `notebooks/` — exploração e experimentos interativos
- `src/` — código fonte (subpastas: `data`, `models`, `api`, `evaluation`)
- `models/` — artefatos e checkpoints
- `mlruns/` — rastreamento do MLflow
- `tests/` — testes automatizados

## Dataset

Descreva aqui o dataset usado (colunas principais, fonte, tamanho, problema de classificação). Se houver arquivos na pasta `data/raw/`, informe-os ou cole o README do dataset.

## Como rodar (pré-requisitos)

- Python 3.9+ (recomenda-se criar um venv)
- Instalar dependências:

```bash
python -m pip install -r requirements.txt
```

## Comandos úteis

- Preparar os dados:

```bash
python -m src.data.prepare --input data/raw --output data/processed
```

- Treinar modelo:

```bash
python -m src.models.train --config configs/train.yaml
```

- Avaliar modelo:

```bash
python -m src.evaluation.evaluate --model models/checkpoint.pt --data data/processed
```

- Rodar API localmente:

```bash
uvicorn src.api.app:app --reload
```

## Arquitetura do modelo

Descreva aqui a arquitetura da MLP e dos baselines (features de entrada, camadas, funções de ativação, hiperparâmetros importantes).

## Métricas de avaliação

Utilizamos as seguintes métricas para o problema de classificação binária: AUC-ROC, precisão, recall, F1-score e matriz de confusão.

## Rastreamento e reprodutibilidade

O projeto usa MLflow para registrar parâmetros, métricas e artefatos. Exemplos de comandos para iniciar tracking local:

```bash
mlflow ui --backend-store-uri mlruns
```

## Deploy

Descrição breve do processo de deploy (containerização com Docker, endpoint em FastAPI, orientações para nuvem).

## Como contribuir

- Abra uma issue descrevendo a melhoria ou bug
- Crie um branch com a alteração (`feature/descricao`)
- Submeta um pull request com testes que validem a mudança

## Contato

Autor: Rafael (contato: inserir e-mail)

## Licença

Adicionar a licença do projeto (por exemplo, MIT).

