from app.engine.calculator import calculate_projections


def test_calculate_projections():
    # This example checks revenue over a twelve-month horizon only.
    res = calculate_projections(
        100, 1500, 0.05, 0.02, 12,
        monthly_fixed_cost=0, monthly_cost_per_customer=0,
    )
    assert len(res) == 12
    assert res[0]["customers"] == 100
    assert res[0]["revenue"] == 150000.0  # 100 * 1500
    assert res[0]["total_cost"] == 0
    assert res[0]["modelled_profit"] == 150000.0
