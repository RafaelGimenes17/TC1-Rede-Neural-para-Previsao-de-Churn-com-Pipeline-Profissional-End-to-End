"""
tests/conftest.py
Fixtures compartilhadas entre todos os testes.
"""

import textwrap

import numpy as np
import pandas as pd
import pytest

TELCO_CSV = textwrap.dedent("""\
    customerID,gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges,Churn
    A001,Female,0,Yes,No,12,Yes,No,DSL,Yes,No,Yes,No,No,No,One year,Yes,Bank transfer (automatic),50.0,600.0,No
    A002,Male,1,No,No,1,Yes,No,Fiber optic,No,No,No,No,Yes,Yes,Month-to-month,Yes,Electronic check,85.0, ,Yes
    A003,Female,0,Yes,Yes,60,Yes,Yes,DSL,Yes,Yes,Yes,Yes,Yes,Yes,Two year,No,Credit card (automatic),75.0,4500.0,No
    A004,Male,0,No,No,24,No,No phone service,No,No internet service,No internet service,No internet service,No internet service,No internet service,No internet service,One year,No,Mailed check,20.0,480.0,No
    A005,Male,1,Yes,No,3,Yes,Yes,Fiber optic,No,Yes,No,No,Yes,No,Month-to-month,Yes,Electronic check,90.0,270.0,Yes
""")


@pytest.fixture
def raw_csv_path(tmp_path) -> str:
    """Cria um CSV sintético com estrutura idêntica ao dataset Telco."""
    csv_file = tmp_path / "telco.csv"
    csv_file.write_text(TELCO_CSV, encoding="utf-8")
    return str(csv_file)


@pytest.fixture
def loaded_df(raw_csv_path) -> pd.DataFrame:
    """DataFrame já processado por load_raw."""
    from src.data.loader import load_raw
    return load_raw(raw_csv_path)


@pytest.fixture
def binary_arrays() -> tuple[np.ndarray, np.ndarray]:
    """Par (y_true, y_prob) para testar compute_metrics."""
    rng = np.random.default_rng(42)
    y_true = np.array([0, 0, 1, 1, 0, 1, 0, 1, 1, 0])
    y_prob = rng.uniform(0, 1, size=len(y_true))
    # Garante discriminação suficiente para roc_auc_score não lançar exceção
    y_prob[y_true == 1] = np.clip(y_prob[y_true == 1] + 0.3, 0, 1)
    return y_true, y_prob
