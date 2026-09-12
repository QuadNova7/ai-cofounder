from copy import deepcopy
from unittest.mock import patch

import pytest

from app.engine.calculator import calculate_projections
from app.engine.sensitivity import calculate_price_sensitivity


@pytest.fixture
def inputs():
    return dict(
        starting_customers=100, monthly_price=1500,
        growth_rate=0, churn_rate=0, months=3,
        monthly_fixed_cost=50000, monthly_cost_per_customer=400,
    )


def test_manual_three_month_example(inputs):
    results = calculate_price_sensitivity(**inputs)
    expected = [
        (-0.1, 1350, 405000, 270000, 135000, -45000),
        (0, 1500, 450000, 270000, 180000, 0),
        (0.1, 1650, 495000, 270000, 225000, 45000),
    ]
    keys = (
        'price_percentage_change', 'adjusted_monthly_price', 'total_revenue',
        'total_costs', 'total_modelled_profit', 'profit_difference_from_baseline',
    )
    assert len(results) == 3
    for result, values in zip(results, expected):
        assert result == pytest.approx(dict(zip(keys, values)))


@pytest.mark.parametrize('changes,expected', [
    ([-0.25, 0.5], [-0.25, 0.5, 0]),
    ([0, 0.0, -0.0, 0.5, 0.5], [0, 0.5]),
    ([], [0]),
])
def test_custom_changes_and_unique_baseline(inputs, changes, expected):
    results = calculate_price_sensitivity(**inputs, price_percentage_changes=changes)
    assert [row['price_percentage_change'] for row in results] == expected
    for row in results:
        change = row['price_percentage_change']
        assert row['adjusted_monthly_price'] == pytest.approx(1500 * (1 + change))
        assert row['profit_difference_from_baseline'] == pytest.approx(450000 * change)


@pytest.mark.parametrize('field,total_costs', [
    ('starting_customers', 150000), ('monthly_price', 270000),
])
def test_zero_customers_or_price(inputs, field, total_costs):
    inputs[field] = 0
    for row in calculate_price_sensitivity(**inputs):
        assert row['total_revenue'] == 0
        assert row['total_costs'] == total_costs
        assert row['total_modelled_profit'] == -total_costs
        assert row['profit_difference_from_baseline'] == 0
        if field == 'monthly_price':
            assert row['adjusted_monthly_price'] == 0


def test_full_price_reduction(inputs):
    result, baseline = calculate_price_sensitivity(**inputs, price_percentage_changes=[-1])
    assert result['adjusted_monthly_price'] == 0
    assert result['total_revenue'] == 0
    assert result['total_costs'] == 270000
    assert result['total_modelled_profit'] == -270000
    assert result['profit_difference_from_baseline'] == -450000
    assert baseline['price_percentage_change'] == 0


@pytest.mark.parametrize('change', [
    True, False, '0.1', None, complex(1, 2), [], {},
    float('nan'), float('inf'), float('-inf'), -1.001,
])
def test_invalid_changes(inputs, change):
    with pytest.raises(ValueError, match='price_percentage_changes'):
        calculate_price_sensitivity(**inputs, price_percentage_changes=[0, change])


@pytest.mark.parametrize('field,value,error', [
    ('starting_customers', True, TypeError), ('starting_customers', -1, ValueError),
    ('months', 1.5, TypeError), ('months', 0, ValueError),
    ('monthly_price', True, ValueError), ('monthly_price', -10, ValueError),
    ('monthly_fixed_cost', -1, ValueError),
    ('monthly_cost_per_customer', float('nan'), ValueError),
    ('growth_rate', -0.1, ValueError), ('churn_rate', 1.1, ValueError),
])
def test_projection_validation_is_reused(inputs, field, value, error):
    inputs[field] = value
    with pytest.raises(error):
        calculate_price_sensitivity(**inputs, price_percentage_changes=[-1])


def test_inputs_unchanged(inputs):
    inputs['price_percentage_changes'] = [0.2, 0, 0, -0.1]
    original = deepcopy(inputs)
    calculate_price_sensitivity(**inputs)
    assert inputs == original


def test_only_price_changes_and_each_case_uses_projections(inputs):
    inputs.update(starting_customers=3, growth_rate=0.5, churn_rate=0.1,
                  monthly_price=19.99)
    with patch('app.engine.sensitivity.calculate_projections',
               wraps=calculate_projections) as project:
        results = calculate_price_sensitivity(**inputs)
    assert project.call_count == 3
    for call in project.call_args_list:
        actual = dict(call.kwargs)
        actual.pop('monthly_price')
        assert actual == {key: value for key, value in inputs.items() if key != 'monthly_price'}
    for row in results:
        monthly = calculate_projections(**{
            **inputs, 'monthly_price': row['adjusted_monthly_price'],
        })
        for total_key, month_key in [
            ('total_revenue', 'revenue'), ('total_costs', 'total_cost'),
            ('total_modelled_profit', 'modelled_profit'),
        ]:
            assert row[total_key] == pytest.approx(sum(m[month_key] for m in monthly))


def test_default_period_and_generator_changes(inputs):
    inputs.pop('months')
    results = calculate_price_sensitivity(
        **inputs, price_percentage_changes=(change for change in [0, 0.25]),
    )
    assert results[0]['total_revenue'] == 1800000
    assert results[1]['total_revenue'] == 2250000
