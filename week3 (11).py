# -*- coding: utf-8 -*-
"""Week3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rnrJR4V84cDrdxjG622RsWpcRjEimdFW

# 1. Transportation Problem: Optimal Shipping Plan
"""

pip install pulp

import pulp

# 1. Define Warehouses (sources) and their supply
warehouses = ['W1', 'W2', 'W3']
supply = {
    'W1': 250,
    'W2': 250,
    'W3': 50
}

# 2. Define Stores (destinations) and their demand
stores = ['S1', 'S2', 'S3', 'S4']
demand = {
    'S1': 100,
    'S2': 150,
    'S3': 50,
    'S4': 200
}

# 3. Define the cost of shipping each unit from each warehouse to each store
costs = {
    ('W1','S1'):  4,  ('W1','S2'): 11,  ('W1','S3'):  3,  ('W1','S4'):  7,
    ('W2','S1'):  6,  ('W2','S2'):  3,  ('W2','S3'):  7,  ('W2','S4'):  9,
    ('W3','S1'):  5,  ('W3','S2'):  8,  ('W3','S3'): 12,  ('W3','S4'): 10
}

# 4. Initialize the LP problem
model = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# 5. Create a dictionary of decision variables x[w, s]
#    Each x[w, s] >= 0, representing how many units to ship from warehouse w to store s
x = pulp.LpVariable.dicts(
    "ship",
    [(w, s) for w in warehouses for s in stores],
    lowBound=0,
    cat=pulp.LpInteger   # or LpContinuous if fractional shipping is allowed
)

#6. Define the objective function: minimize sum of cost * quantity shipped
model += pulp.lpSum(costs[(w,s)] * x[(w,s)] for w in warehouses for s in stores), "Total_Transportation_Cost"

# 7. Supply constraints: sum of shipments from each warehouse cannot exceed its supply
for w in warehouses:
    model += pulp.lpSum(x[(w,s)] for s in stores) <= supply[w], f"Supply_{w}"

# 8. Demand constraints: sum of shipments to each store must meet its demand
for s in stores:
    model += pulp.lpSum(x[(w,s)] for w in warehouses) == demand[s], f"Demand_{s}"

# 9. Solve the model
model.solve(pulp.PULP_CBC_CMD(msg=0))

# 10. Print the results
print("Status:", pulp.LpStatus[model.status])
print("Optimal Cost = ", pulp.value(model.objective))

# Print each decision variable’s optimal value
for w in warehouses:
    for s in stores:
        if x[(w,s)].varValue > 0:
            print(f"Ship {x[(w,s)].varValue} units from {w} to {s}")

"""**Key Observations**

**Demands are met exactly**

S1 demand (100 units) is fulfilled by 50 units from W2 and 50 units from W3.

S2 demand (150 units) is fulfilled by 150 units from W2.

S3 demand (50 units) is fulfilled by 50 units from W1.

S4 demand (200 units) is fulfilled by 200 units from W1.  

   




**Supplies are fully (or nearly) utilized**

W1 supply (250 units) is used up by sending 50 to S3 and 200 to S4.

W2 supply (250 units) uses only 200 units (50 to S1 + 150 to S2), so there is a little unused capacity (50 units) there.

W3 supply (50 units) is fully used by sending 50 to S1.  

**Total Cost Calculation**

𝑊
1
→
𝑆
3
W1→S3: 50 units × $3 = $150

𝑊
1
→
𝑆
4
W1→S4: 200 units × $7 = $1{,}400

𝑊
2
→
𝑆
1
W2→S1: 50 units × $6 = $300

**𝑊**
2
→
𝑆
2
W2→S2: 150 units × $3 = $450

𝑊
3
→
𝑆
1
W3→S1: 50 units × $5 = $250

Total = $150 + $1{,}400 + $300 + $450 + $250 = $2{,}550

# Interpretation

This shipping plan minimizes the total transportation cost while meeting all store demands and not exceeding the warehouses’ supplies.

Notice that W2 is not fully utilized because the solver found that routing extra units from W2 to other stores would be more expensive than using W1 or W3 for those demands.

The solution makes strategic use of the lower-cost routes (e.g., W1→S3 at $3/unit) and avoids higher-cost combinations.
"""



"""2. Manufacturing Problem: Maximizing Profit (Product Mix)

"""

import pulp

# 1. Create the problem: we are maximizing profit
model = pulp.LpProblem("Product_Mix_Problem", pulp.LpMaximize)

# 2. Define the decision variables: x1 (units of A) and x2 (units of B)
#    Use LpContinuous if fractional units are allowed; use LpInteger if not.
x1 = pulp.LpVariable('x1', lowBound=0, cat=pulp.LpContinuous)
x2 = pulp.LpVariable('x2', lowBound=0, cat=pulp.LpContinuous)

# 3. Define the objective function: Maximize 50*x1 + 80*x2
model += 50 * x1 + 80 * x2, "Total_Profit"

# 4. Add the constraints
#    Machine M1 capacity: 3x1 + 5x2 <= 600
model += 3 * x1 + 5 * x2 <= 600, "M1_Capacity"

#    Machine M2 capacity: 2x1 + 4x2 <= 500
model += 2 * x1 + 4 * x2 <= 500, "M2_Capacity"

# 5. Solve the problem
model.solve(pulp.PULP_CBC_CMD(msg=0))

# 6. Print the results
print("Status:", pulp.LpStatus[model.status])
print("Optimal Solution Found:")
print(f"  x1 (Product A) = {x1.varValue}")
print(f"  x2 (Product B) = {x2.varValue}")
print("Maximum Profit = $", pulp.value(model.objective))

"""**Key Observations**

**Machine Capacities Used**

Machine M1 (600 hours): Producing 200 units of A uses
3
×
200
=
600
3×200=600 hours, fully occupying M1.

Machine M2 (500 hours): Producing 200 units of A uses
2
×
200
=
400
2×200=400 hours, leaving 100 hours unused.

# Why No Product B?

Although product B has a higher profit per unit ($80 vs. $50 for A), it also consumes more hours on both machines (5 hours on M1 and 4 hours on M2).

Machine M1 is the “bottleneck” here: If you try to produce B, you quickly use up M1’s capacity without achieving a higher total profit than focusing on A.

## Profit Calculation

Profit from A = $50 × 200 = $10,000

Profit from B = $80 × 0 = $0

Total = $10,000

# Interpretation

The optimal strategy is to produce only Product A and fully utilize Machine M1 while partially using Machine M2.

The leftover 100 hours on M2 cannot be used effectively to produce B, because M1 is already at capacity (600 hours).

In business terms, Product A gives a better overall return when you consider both machines’ time constraints.
"""





"""# 3. Manufacturing Problem: Minimizing Production Cost

"""

from pulp import LpProblem, LpVariable, LpMinimize, value

# Define the LP problem
problem = LpProblem("Minimize_Production_Cost", LpMinimize)

#Define decision variables (number of chairs and tables)
x1 = LpVariable("Chairs", lowBound=0, cat="Continuous")  # x1 >= 0
x2 = LpVariable("Tables", lowBound=0, cat="Continuous")  # x2 >= 0

# Define the objective function (Minimize cost)
problem += 30*x1 + 50*x2, "Total Cost"

# Define constraints
problem += 5*x1 + 8*x2 <= 800, "Wood Constraint"
problem += 2*x1 + 3*x2 <= 300, "Labor Constraint"

# Solve the problem
problem.solve()

# Print results
print("Status:", problem.status)  # 1 means Optimal
print("Optimal Solution:")
print("  Number of Chairs (x1) =", value(x1))
print("  Number of Tables (x2) =", value(x2))
print("Minimum Production Cost = $", value(problem.objective))

"""The solver found that the optimal solution is to produce 0 chairs and 0 tables.  

This results in a minimum production cost of $0.  

The reason is that any production would violate the given resource constraints (wood and labor availability).  

Since the objective is to minimize cost, the solver chooses not to produce anything to keep costs at their lowest.  

# Conclusion:
The company cannot produce any chairs or tables with the given wood and labor limits. To enable production, either resource availability needs to increase or product requirements need to be adjusted.
"""

