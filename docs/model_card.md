# Model Card — Churn MLP PyTorch

## Visão Geral do Modelo

| Campo | Valor |
|---|---|
| **Nome** | ChurnMLP |
| **Versão** | 0.1.0 |
| **Tipo** | Classificação binária supervisionada |
| **Framework** | PyTorch 2.x |
| **Data de treinamento** | Junho/2025 |
| **Responsáveis** | Equipe TC1 — FIAP MBA IA para Devs |

### Arquitetura

```
Input (46 features após OHE)
  → Linear(128) → BatchNorm1d → ReLU → Dropout(0.3)
  → Linear(64)  → BatchNorm1d → ReLU → Dropout(0.3)
  → Linear(32)  → BatchNorm1d → ReLU → Dropout(0.3)
  → Linear(1)   → [logits]
```

- **Loss:** `BCEWithLogitsLoss` com `pos_weight ≈ 2.77` (compensa o desbalanceamento de classes)
- **Otimizador:** Adam (`lr=1e-3`, `weight_decay=1e-4`)
- **Early stopping:** paciência de 15 épocas monitorando AUC-ROC de validação; restaura melhores pesos
- **Parâmetros treináveis:** 16.833

---

## Uso Pretendido

### Uso Primário

Prever a probabilidade de churn (cancelamento) de clientes de uma operadora de telecomunicações com base em características contratuais e de consumo. A saída é consumida pela equipe de CRM para priorizar ações de retenção proativa.

### Usuários Pretendidos

- Equipes de CRM e retenção de clientes
- Analistas de negócio que interpretam scores de risco
- Plataforma interna de decisão via API REST

### Uso Fora do Escopo

- Não deve ser usado como único critério para cancelamento de serviços
- Não adequado para segmentos fora do contexto de telecomunicações norte-americanas
- Não deve ser usado para decisões que impactem privacidade ou crédito sem revisão humana

---

## Dados de Treinamento

| Atributo | Valor |
|---|---|
| **Dataset** | Telco Customer Churn (IBM / Kaggle) |
| **Registros** | 7.043 clientes |
| **Features originais** | 20 (3 numéricas + 16 categóricas + 1 target) |
| **Features após pré-processamento** | 46 (StandardScaler + OneHotEncoder) |
| **Taxa de churn** | 26,5% (desbalanceado) |
| **Split** | 70% treino / 15% validação / 15% teste (StratifiedShuffleSplit) |
| **Seed** | 42 |

### Principais Features

| Feature | Tipo | Importância (EDA) |
|---|---|---|
| `Contract` | Categórica | Alta — Month-to-month: ~42% churn |
| `tenure` | Numérica | Alta — 0–6 meses: ~48% churn |
| `InternetService` | Categórica | Alta — Fiber optic: ~42% churn |
| `TechSupport` | Categórica | Média |
| `OnlineSecurity` | Categórica | Média |
| `MonthlyCharges` | Numérica | Média |

### Pré-processamento

```python
ColumnTransformer([
    ('num', StandardScaler(), ['tenure', 'MonthlyCharges', 'TotalCharges']),
    ('cat', OneHotEncoder(handle_unknown='ignore'), CATEGORICAL_FEATURES),
])
```

---

## Performance

Avaliação no conjunto de **teste** (1.057 amostras, nunca vistas durante treino ou validação).

| Modelo | AUC-ROC | PR-AUC | Recall | F1 | Precisão |
|---|---|---|---|---|---|
| **MLP PyTorch** | **0.8456** | **0.6447** | **0.8321** | **0.6148** | **0.4874** |
| LogisticRegression | 0.8490 | 0.6409 | 0.8107 | 0.6245 | 0.5078 |
| GradientBoosting | 0.8467 | 0.6539 | 0.5179 | 0.5788 | 0.6561 |
| RandomForest | 0.8233 | 0.6080 | 0.6750 | 0.6117 | 0.5592 |
| DummyClassifier | 0.4759 | 0.2568 | 0.2286 | 0.2290 | 0.2294 |

> O MLP foi selecionado como modelo de produção pelo **maior Recall (0.8321)**, métrica prioritária dado que o custo de um Falso Negativo (cliente que churnará sem intervenção) é ~30× maior que um Falso Positivo (campanha desnecessária).

### Threshold de Decisão

O limiar de 0.5 foi substituído pelo **threshold ótimo de custo**, calculado varrendo 91 limiares (0.05–0.95) e minimizando:

```
custo_total = FP × $10 + FN × $300
```

O threshold ótimo é menor que 0.5, priorizando Recall em detrimento de Precisão.

### Metas de SLO

| Métrica | Meta | Status |
|---|---|---|
| AUC-ROC (produção) | ≥ 0,78 | ✅ |
| Recall (classe positiva) | ≥ 0,70 | ✅ |
| PR-AUC | ≥ 0,60 | ✅ |
| Latência API (p95) | ≤ 500 ms | A verificar em produção |
| Disponibilidade | ≥ 99,5% | A verificar em produção |

---

## Análise de Custo — FP vs FN

| Erro | Situação | Custo estimado |
|---|---|---|
| **Falso Positivo (FP)** | Cliente contatado que não ia churnar | $10 (campanha desnecessária) |
| **Falso Negativo (FN)** | Cliente churnou sem intervenção | $300 (receita mensal perdida) |

**Premissas do cálculo:**
- Ticket médio mensal: $64,76
- Duração de retenção bem-sucedida: 6 meses
- Taxa de sucesso da campanha: 30%
- Custo da campanha por cliente: $15,00

Cálculo completo disponível em `notebooks/03_mlp.ipynb` (Seção 5) e `docs/analise_custo.png`.

---

## Limitações e Vieses

- **Escopo geográfico:** Dataset de operadora norte-americana; performance pode ser inferior em outros mercados
- **Dados estáticos:** Não captura comportamento temporal do cliente (séries temporais)
- **Features ausentes:** Sem dados de satisfação (NPS, tickets de suporte), que são preditores fortes de churn
- **Desbalanceamento:** Apenas 26,5% de positivos; o modelo usa `pos_weight` para compensar, mas pode haver viés em segmentos sub-representados
- **Drift:** O modelo foi treinado em dados de um período específico; performance pode degradar com mudanças no comportamento dos clientes

---

## Plano de Monitoramento

| Evento | Ação |
|---|---|
| AUC-ROC em produção cai ≥ 3 pp | Retreinar com dados mais recentes |
| Distribuição de features desvia > 2σ | Alertar equipe de ML (data drift) |
| Recall < 0.65 | Revisão imediata do threshold |
| A cada 90 dias | Retreino preventivo com novos dados |

**Métricas a monitorar em produção:**
- AUC-ROC e Recall no conjunto de avaliação mensal
- Distribuição de `churn_probability` (deve ser estável)
- Taxa de churn observada vs. predita (calibração)
- Tempo de inferência por requisição (latência p50/p95/p99)

---

## Informações Éticas

- **Privacidade:** O modelo não utiliza dados de identificação pessoal (PII) — o campo `customerID` é descartado no pré-processamento
- **Equidade:** Não foram realizadas análises de fairness por subgrupos (gênero, idade). Recomenda-se auditoria antes de usar em decisões que afetem grupos protegidos
- **Transparência:** Todos os experimentos estão registrados no MLflow (`notebooks/mlruns/`), garantindo rastreabilidade completa
- **Supervisão humana:** Scores de risco devem ser revisados pela equipe de CRM antes de ações de retenção automatizadas

---

## Artefatos

| Arquivo | Descrição |
|---|---|
| `models/artifacts/mlp_weights.pt` | Pesos do modelo PyTorch |
| `models/artifacts/preprocessor.joblib` | Pipeline sklearn de pré-processamento |
| `models/artifacts/model_config.json` | Metadados: arquitetura, threshold, métricas |
| `notebooks/mlruns/` | Experimentos MLflow (todos os modelos) |
| `docs/comparacao_modelos.png` | Gráfico comparativo de modelos |
| `docs/analise_custo.png` | Curva de custo vs. threshold |

---

## Citação

```
Gimenes, R. F. et al. (2025). Rede Neural para Previsão de Churn com Pipeline Profissional End-to-End.
FIAP MBA IA para Devs — Tech Challenge 1, Módulo 1.
```
