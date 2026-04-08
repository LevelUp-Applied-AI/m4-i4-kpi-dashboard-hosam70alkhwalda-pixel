"""Tests for the KPI dashboard analysis.

Write at least 3 tests:
1. test_extraction_returns_dataframes — extract_data returns a dict of DataFrames
2. test_kpi_computation_returns_expected_keys — compute_kpis returns a dict with your 5 KPI names
3. test_statistical_test_returns_pvalue — run_statistical_tests returns results with p-values
"""
import pytest
import pandas as pd
from analysis import connect_db, extract_data, compute_kpis, run_statistical_tests


def test_extraction_returns_dataframes():
    """Connect to the database, extract data, and verify the result is a dict of DataFrames."""
    engine = connect_db()
    data = extract_data(engine)

    assert isinstance(data, dict)

    expected_tables = ["customers", "products", "orders", "order_items"]

    for table in expected_tables:
        assert table in data
        assert isinstance(data[table], pd.DataFrame)
        assert not data[table].empty


def test_kpi_computation_returns_expected_keys():
    """Compute KPIs and verify the result contains all expected KPI names."""
    engine = connect_db()
    data = extract_data(engine)
    kpis = compute_kpis(data)

    assert isinstance(kpis, dict)

    expected_kpis = [
        "monthly_revenue",
        "weekly_orders",
        "revenue_by_city",
        "aov_by_category",
        "customer_purchase_frequency"
    ]

    for kpi in expected_kpis:
        assert kpi in kpis


def test_statistical_test_returns_pvalue():
    """Run statistical tests and verify results include p-values."""
    engine = connect_db()
    data = extract_data(engine)
    stats_results = run_statistical_tests(data)

    assert isinstance(stats_results, dict)

  
    found_pvalue = False

    for test in stats_results.values():
        if "p_value" in test:
            p = test["p_value"]
            assert 0 <= p <= 1
            found_pvalue = True

    assert found_pvalue