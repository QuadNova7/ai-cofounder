# Deterministic Financial Calculation Engine
import math
def calculate_projections(
    starting_customers: int,
    monthly_price: float,
    growth_rate: float,
    churn_rate: float,
    months: int = 12,
    *,
    monthly_fixed_cost: float,
    monthly_cost_per_customer: float,
):
    if isinstance(starting_customers, bool) or not isinstance(starting_customers, int):
        raise TypeError("starting_customers must be an integer")

    if starting_customers < 0:
        raise ValueError("starting_customers cannot be negative")

    if isinstance(months, bool) or not isinstance(months, int):
        raise TypeError("months must be an integer")

    if months < 1:
        raise ValueError("months must be at least 1")

    for name, rate in {
        "growth_rate": growth_rate,
        "churn_rate": churn_rate,
    }.items():
        if (
            isinstance(rate, bool)
            or not isinstance(rate, (int, float))
            or not math.isfinite(rate)
            or rate < 0
        ):
            raise ValueError(f"{name} must be a finite, non-negative number")

    if churn_rate > 1:
        raise ValueError("churn_rate cannot exceed 1")

    projections = []
    customers = starting_customers

    for month in range(1, months + 1):
        # Calculate this month's revenue, costs, and profit.
        result = calculate_subscription_month(
            monthly_price=monthly_price,
            paying_customer=customers,
            monthly_fixed_cost=monthly_fixed_cost,
            monthly_cost_per_customer=monthly_cost_per_customer,
        )

        # Store the month, customers, and all calculator outputs.
        projections.append({
            "month": month,
            "customers": customers,
            **result,
        })

        # Round to whole customers for the next month.
        if month < months:
            customers = round(customers * (1 + growth_rate - churn_rate))

    return projections




def is_valid_money(x):
    return (
        not isinstance(x, bool)
        and isinstance(x, (int, float))
        and x >= 0
        and math.isfinite(x)
    )




 


def calculate_subscription_month(
        monthly_price :float,
        paying_customer:int,
        monthly_fixed_cost:float,
        monthly_cost_per_customer:float,

        
):
    if isinstance(paying_customer, bool) or not isinstance(paying_customer, int):
        raise TypeError("paying_customer must be an integer")

    if paying_customer < 0:
        raise ValueError("paying_customer cannot be negative")

    # Validate each monetary input.
    money_inputs = {
        "monthly_price": monthly_price,
        "monthly_fixed_cost": monthly_fixed_cost,
        "monthly_cost_per_customer": monthly_cost_per_customer,
    }

    for name, value in money_inputs.items():
        if not is_valid_money(value):
            raise ValueError(f"{name} must be a finite, non-negative number")

    


    

    
    


    #caculate revenue 
    revenue = monthly_price*paying_customer

    #calculate varaible cost
    variable_cost = monthly_cost_per_customer * paying_customer

    #calculate total cost
    total_cost = monthly_fixed_cost + variable_cost

    #calculate profit 
    profit = revenue - total_cost

    return {
        "revenue": revenue,
        "variable_cost": variable_cost,
        "total_cost": total_cost,
        "modelled_profit": profit,
    }



