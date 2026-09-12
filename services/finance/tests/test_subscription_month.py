
import pytest

from app.engine.calculator import calculate_subscription_month


@pytest.mark.parametrize(
    "price, customers, fixed_cost, cost_per_customer, expected",
    [
        pytest.param(
            1500, 100, 50000, 400,
            {"revenue": 150000, "variable_cost": 40000,
             "total_cost": 90000, "modelled_profit": 60000},
            id="profitable-business",
        ),
        pytest.param(
            1500, 0, 50000, 400,
            {"revenue": 0, "variable_cost": 0,
             "total_cost": 50000, "modelled_profit": -50000},
            id="zero-customers-fixed-cost-remains",
        ),
        pytest.param(
            1000, 100, 60000, 400,
            {"revenue": 100000, "variable_cost": 40000,
             "total_cost": 100000, "modelled_profit": 0},
            id="break-even",
        ),
        pytest.param(
            500, 100, 50000, 400,
            {"revenue": 50000, "variable_cost": 40000,
             "total_cost": 90000, "modelled_profit": -40000},
            id="loss-making-business",
        ),
        pytest.param(
            0, 0, 0, 0,
            {"revenue": 0, "variable_cost": 0,
             "total_cost": 0, "modelled_profit": 0},
            id="all-zero-inputs",
        ),
        pytest.param(
            19.99, 3, 10.50, 2.25,
            {"revenue": 59.97, "variable_cost": 6.75,
             "total_cost": 17.25, "modelled_profit": 42.72},
            id="fractional-money-amounts",
        ),
    ],
)
def test_calculate_subscription_month(
    price, customers, fixed_cost, cost_per_customer, expected
):
    # Positional arguments support the current paying_customer parameter name.
    result = calculate_subscription_month(
        price, customers, fixed_cost, cost_per_customer
    )

    # approx tolerates normal floating-point representation differences.
    assert result == pytest.approx(expected)
