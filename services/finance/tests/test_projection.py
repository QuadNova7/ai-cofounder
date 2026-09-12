"""Scenario expectations calculated by hand, independently of the calculator."""

from copy import deepcopy

import pytest

from app.engine.scenario_engine import calculate_scenarios
from app.interface import run_revenue_estimation
from shared.contracts.business_model import BusinessModelCanvas, BusinessModelOutput
from shared.contracts.idea import IdeaAnalysisOutput
from shared.contracts.market import MarketResearchOutput


@pytest.fixture
def assumptions():
    return {
        'conservative': dict(starting_customers=10, monthly_price=100,
                             growth_rate=0.2, churn_rate=0, months=3,
                             monthly_fixed_cost=200, monthly_cost_per_customer=20),
        'moderate': dict(starting_customers=20, monthly_price=50,
                         growth_rate=0, churn_rate=0.5, months=3,
                         monthly_fixed_cost=300, monthly_cost_per_customer=10),
        'optimistic': dict(starting_customers=5, monthly_price=10,
                           growth_rate=0, churn_rate=0, months=3,
                           monthly_fixed_cost=100, monthly_cost_per_customer=4),
    }


def assert_months(actual, expected):
    assert len(actual) == len(expected)
    for number, (row, values) in enumerate(zip(actual, expected), 1):
        customers, revenue, variable_cost, total_cost, profit = values
        assert row == pytest.approx(dict(
            month=number, customers=customers, revenue=revenue,
            variable_cost=variable_cost, total_cost=total_cost, modelled_profit=profit,
        ))
        assert type(row['customers']) is int


def test_three_scenarios_use_independent_assumptions(assumptions):
    results = calculate_scenarios(**assumptions)
    assert list(results) == ['conservative', 'moderate', 'optimistic']
    # 10 -> 12 -> round(14.4)=14 customers; costs = 200 + 20 * customers.
    assert_months(results['conservative'], [
        (10, 1000, 200, 400, 600), (12, 1200, 240, 440, 760),
        (14, 1400, 280, 480, 920),
    ])
    # Half the remaining customers churn each month.
    assert_months(results['moderate'], [
        (20, 1000, 200, 500, 500), (10, 500, 100, 400, 100),
        (5, 250, 50, 350, -100),
    ])
    # The name does not guarantee profitability or relative ordering.
    assert_months(results['optimistic'], [(5, 50, 20, 120, -70)] * 3)


def test_zero_customers_keep_each_scenarios_fixed_costs(assumptions):
    for inputs in assumptions.values():
        inputs['starting_customers'] = 0
    results = calculate_scenarios(**assumptions)
    for name, cost in [('conservative', 200), ('moderate', 300), ('optimistic', 100)]:
        assert_months(results[name], [(0, 0, 0, cost, -cost)] * 3)


@pytest.mark.parametrize('name', ['conservative', 'moderate', 'optimistic'])
@pytest.mark.parametrize('field,value,error', [
    ('starting_customers', True, TypeError),
    ('starting_customers', -1, ValueError),
    ('months', 0, ValueError),
    ('months', 1.5, TypeError),
    ('monthly_price', -1, ValueError),
    ('monthly_fixed_cost', float('nan'), ValueError),
    ('monthly_cost_per_customer', float('inf'), ValueError),
    ('growth_rate', -0.1, ValueError),
    ('churn_rate', 1.1, ValueError),
])
def test_invalid_scenario_inputs(assumptions, name, field, value, error):
    assumptions[name][field] = value
    with pytest.raises(error, match=f'{name}: .*{field}'):
        calculate_scenarios(**assumptions)


@pytest.mark.parametrize('field', ['monthly_fixed_cost', 'monthly_cost_per_customer'])
def test_scenario_costs_are_required(assumptions, field):
    del assumptions['moderate'][field]
    with pytest.raises(TypeError, match=f'moderate: .*{field}'):
        calculate_scenarios(**assumptions)


def test_invalid_scenario_container(assumptions):
    assumptions['optimistic'] = None
    with pytest.raises(TypeError, match='optimistic: scenario inputs must be a dictionary'):
        calculate_scenarios(**assumptions)


def test_scenarios_preserve_inputs_and_isolate_results(assumptions):
    original = deepcopy(assumptions)
    results = calculate_scenarios(**assumptions)
    assert assumptions == original
    untouched = deepcopy(results)
    results['conservative'][0]['revenue'] = -999
    assert results['moderate'] == untouched['moderate']
    assert results['optimistic'] == untouched['optimistic']
    assert results['conservative'][1:] == untouched['conservative'][1:]
    assert calculate_scenarios(**assumptions) == untouched
    assert assumptions == original


def test_shared_input_dictionary_does_not_share_results(assumptions):
    inputs = assumptions['conservative']
    original = deepcopy(inputs)
    results = calculate_scenarios(conservative=inputs, moderate=inputs, optimistic=inputs)
    results['conservative'][0]['customers'] = 999
    assert results['moderate'][0]['customers'] == 10
    assert results['optimistic'][0]['customers'] == 10
    assert inputs == original


def test_revenue_interface_forwards_existing_costs_and_scenario_rates():
    idea = IdeaAnalysisOutput(
        problem_statement='Example', target_users=[], refined_value_proposition='Example',
        key_assumptions=[], clarity_score=0.5, feasibility_score=0.5, confidence_score=0.5,
    )
    market = MarketResearchOutput(
        competitor_landscape=[], customer_personas=[], market_trends=[],
        entry_barriers=[], confidence_score=0.5,
    )
    model = BusinessModelOutput(canvas=BusinessModelCanvas(), confidence_score=0.5)
    original = deepcopy((idea, market, model))
    output = run_revenue_estimation(idea, market, model, horizon_months=3)
    assert [s.scenario_name for s in output.scenarios] == [
        'conservative', 'moderate', 'optimistic',
    ]
    # Net growth .066, .12, .186 gives 25->27->29, 25->28->31, 25->30->36.
    # Revenue = 99 * customers; costs = 5000 + 15 * customers.
    expected = [
        [(25, 2475, 375, 5375, -2900), (27, 2673, 405, 5405, -2732),
         (29, 2871, 435, 5435, -2564)],
        [(25, 2475, 375, 5375, -2900), (28, 2772, 420, 5420, -2648),
         (31, 3069, 465, 5465, -2396)],
        [(25, 2475, 375, 5375, -2900), (30, 2970, 450, 5450, -2480),
         (36, 3564, 540, 5540, -1976)],
    ]
    for scenario, months in zip(output.scenarios, expected):
        assert_months(scenario.monthly_projections, months)
        # Preserve the existing final-month summary behavior for any horizon.
        assert scenario.month_12_customers == months[-1][0]
        assert scenario.month_12_revenue == months[-1][1]
    assert (idea, market, model) == original
