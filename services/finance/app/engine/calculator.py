# Deterministic Financial Calculation Engine
import math
def calculate_projections(starting_customers: int, monthly_price: float, growth_rate: float, churn_rate: float, months: int = 12):
    projections = []
    customers = starting_customers
    for m in range(1, months + 1):
        revenue = customers * monthly_price
        projections.append({
            "month": m,
            "customers": int(customers),
            "revenue": round(revenue, 2)
        })
        customers = customers * (1 + growth_rate - churn_rate)
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



