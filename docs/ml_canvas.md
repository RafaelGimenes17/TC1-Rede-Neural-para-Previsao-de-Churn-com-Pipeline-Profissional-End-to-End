# ML Canvas — Churn Prediction

> Documento de formulação do problema. Preenchido na Etapa 1 antes de qualquer modelagem.

---

## 🎯 Problema de Negócio

Uma operadora de telecomunicações está perdendo clientes em ritmo acelerado.
A diretoria precisa identificar **quais clientes têm risco de cancelamento (churn)**
para que equipes de retenção possam agir preventivamente.

---

## 👥 Stakeholders

| Papel | Interesse |
|---|---|
| Diretoria de Negócios | Reduzir taxa de churn e aumentar LTV |
| Time de CRM / Retenção | Lista priorizada de clientes em risco |
| Time de Dados / MLOps | Modelo estável, reprodutível e monitorado |
| Cliente final | Receber oferta de retenção personalizada |

---

## 📐 Formulação do Problema ML

| Campo | Valor |
|---|---|
| Tipo de problema | Classificação binária supervisionada |
| Target | `Churn` — Yes (1) / No (0) |
| Nível de predição | Por cliente (inferência individual) |
| Frequência de uso | Real-time via API |
| Dataset | Telco Customer Churn — IBM/Kaggle |
| Registros | 7.043 clientes |
| Features | 20 preditoras |

---

## 📊 Métricas Técnicas

| Métrica | Justificativa |
|---|---|
| **AUC-ROC** | Métrica principal — mede capacidade discriminativa independente do threshold |
| **PR-AUC** | Essencial em classes desbalanceadas (~26% positivos) |
| **Recall** | Prioridade — minimizar Falsos Negativos (churners não detectados) |
| **F1-Score** | Equilíbrio entre precision e recall |

---

## 💰 Métricas de Negócio

| Métrica | Fórmula |
|---|---|
| Receita retida pelo modelo | `TP × ticket_médio_mensal × meses_retenção × taxa_sucesso` |
| Custo de falso positivo | `FP × custo_campanha_retenção` |
| ROI do modelo | `(Receita retida − Custo campanhas) / Custo total` |

### Análise de Custo — Trade-off FP vs FN

> Premissas ilustrativas — valores reais devem ser fornecidos pelo time de negócio.

| Parâmetro | Valor |
|---|---|
| Ticket médio mensal | ~$64,76 (média do dataset) |
| Meses retidos após intervenção | 6 |
| Taxa de sucesso da retenção | 30% |
| Custo de campanha por cliente | $15,00 |

| Tipo | Custo estimado |
|---|---|
| Ganho por TP (cliente retido) | ~$116,57 |
| Custo por FP (alarme falso) | ~$15,00 |
| Custo por FN (churn perdido) | ~$388,56 |

**Conclusão:** FN é ~25x mais caro que FP → priorizar **Recall** (threshold ≤ 0.5).

---

## 🎯 SLOs (Service Level Objectives)

| SLO | Valor mínimo |
|---|---|
| AUC-ROC em produção | ≥ 0.78 |
| Recall (classe positiva) | ≥ 0.70 |
| PR-AUC | ≥ 0.60 |
| Latência da API (p95) | ≤ 500ms |
| Disponibilidade da API | ≥ 99.5% |
| Retreino | A cada 90 dias ou quando AUC-ROC cair 3pp |

---

## 🔍 Principais Drivers de Churn (EDA)

1. **Tipo de contrato:** mensais com ~42% churn vs ~3% bianuais
2. **Tenure:** clientes 0–6 meses com ~48% churn — período crítico
3. **Internet Fiber optic:** ~42% churn
4. **Ausência de TechSupport e OnlineSecurity:** correlacionada com churn
5. **MonthlyCharges:** churnou ($74/mês) vs ficou ($61/mês)

---

## ⚠️ Riscos e Limitações

- Dataset de uma única operadora (contexto norte-americano)
- Dados estáticos — não captura comportamento temporal do cliente
- Desbalanceamento de classes (~26% churn)
- Sem variáveis de satisfação (NPS, tickets de suporte)
- Performance pode degradar em mercados com perfil diferente
