import pytest

from app.engine.calculator import calculate_projections


@pytest.fixture
def inputs():
    return dict(
        starting_customers=100,
        monthly_price=1500,
        growth_rate=0.10,
        churn_rate=0.05,
        months=3,
        monthly_fixed_cost=50000,
        monthly_cost_per_customer=400,
    )


def test_three_month_projection(inputs):
    results = calculate_projections(**inputs)
    expected = [
        dict(month=1, customers=100, revenue=150000, variable_cost=40000,
             total_cost=90000, modelled_profit=60000),
        dict(month=2, customers=105, revenue=157500, variable_cost=42000,
             total_cost=92000, modelled_profit=65500),
        dict(month=3, customers=110, revenue=165000, variable_cost=44000,
             total_cost=94000, modelled_profit=71000),
    ]
    assert len(results) == len(expected)
    for actual, wanted in zip(results, expected):
        assert actual == pytest.approx(wanted)
        assert type(actual['customers']) is int


def test_default_projection_is_twelve_months(inputs):
    inputs.pop('months')
    results = calculate_projections(**inputs)
    assert len(results) == 12
    assert [row['month'] for row in results] == list(range(1, 13))


def test_no_growth_or_churn(inputs):
    inputs.update(growth_rate=0, churn_rate=0)
    results = calculate_projections(**inputs)
    assert len(results) == 3
    for row in results:
        assert row['customers'] == 100
        assert row['revenue'] == 150000
        assert row['modelled_profit'] == 60000


def test_zero_customers_still_incur_fixed_cost(inputs):
    inputs['starting_customers'] = 0
    results = calculate_projections(**inputs)
    assert len(results) == 3
    for row in results:
        assert row['customers'] == 0
        assert row['revenue'] == 0
        assert row['variable_cost'] == 0
        assert row['total_cost'] == 50000
        assert row['modelled_profit'] == -50000


def test_full_churn_affects_next_month(inputs):
    inputs.update(growth_rate=0, churn_rate=1)
    results = calculate_projections(**inputs)
    assert [row['customers'] for row in results] == [100, 0, 0]
    assert [row['modelled_profit'] for row in results] == [60000, -50000, -50000]


def test_fractional_money_one_month(inputs):
    inputs.update(starting_customers=3, monthly_price=19.99, months=1,
                  monthly_fixed_cost=10.50, monthly_cost_per_customer=2.25)
    results = calculate_projections(**inputs)
    assert len(results) == 1
    assert results[0] == pytest.approx(dict(
        month=1, customers=3, revenue=59.97, variable_cost=6.75,
        total_cost=17.25, modelled_profit=42.72,
    ))


def test_rounded_customers_used_for_revenue(inputs):
    # 3 * 1.5 = 4.5 -> 4 (ties to even); then 4 * 1.5 = 6.
    inputs.update(starting_customers=3, growth_rate=0.5, churn_rate=0)
    results = calculate_projections(**inputs)
    assert [row['customers'] for row in results] == [3, 4, 6]
    assert [row['revenue'] for row in results] == [4500, 6000, 9000]


@pytest.mark.parametrize('field', ['starting_customers', 'months'])
@pytest.mark.parametrize('value', [True, False, 2.5, '3', None])
def test_integer_parameters_reject_wrong_types(inputs, field, value):
    inputs[field] = value
    with pytest.raises(TypeError):
        calculate_projections(**inputs)


@pytest.mark.parametrize('field,value', [
    ('starting_customers', -1), ('months', 0), ('months', -1),
])
def test_integer_parameters_reject_invalid_ranges(inputs, field, value):
    inputs[field] = value
    with pytest.raises(ValueError):
        calculate_projections(**inputs)


@pytest.mark.parametrize('field', ['growth_rate', 'churn_rate'])
@pytest.mark.parametrize('value', [-0.1, float('nan'), float('inf'), float('-inf')])
def test_rates_reject_invalid_numbers(inputs, field, value):
    inputs[field] = value
    with pytest.raises(ValueError):
        calculate_projections(**inputs)


@pytest.mark.parametrize('field', ['growth_rate', 'churn_rate'])
@pytest.mark.parametrize('value', [True, False, '0.1', None])
def test_rates_reject_wrong_types(inputs, field, value):
    inputs[field] = value
    # Either convention is acsceptable for type validation.
    with pytest.raises((TypeError, ValueError)):
        calculate_projections(**inputs)


def test_churn_cannot_exceed_one(inputs):
    inputs['churn_rate'] = 1.01
    with pytest.raises(ValueError):
        calculate_projections(**inputs)


def test_growth_can_exceed_one(inputs):
    inputs.update(growth_rate=1.5, churn_rate=0, months=2)
    results = calculate_projections(**inputs)
    assert [row['customers'] for row in results] == [100, 250]


@pytest.mark.parametrize('field', [
    'monthly_price', 'monthly_fixed_cost', 'monthly_cost_per_customer',
])
@pytest.mark.parametrize('value', [-1, float('nan'), float('inf'), True, '100', None])
def test_invalid_money_is_rejected(inputs, field, value):
    inputs[field] = value
    with pytest.raises((TypeError, ValueError)):
        calculate_projections(**inputs)
