# -*- coding: utf-8 -*-
"""Week3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rnrJR4V84cDrdxjG622RsWpcRjEimdFW

1. Transportation Problem: Optimal Shipping Plan
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



"""3. Manufacturing Problem: Minimizing Production Cost

"""

from pulp import LpProblem, LpVariable, LpMinimize, value

# Define the LP problem
problem = LpProblem("Minimize_Production_Cost", LpMinimize)

#Define decision variables (number of chairs and tables)
x1 = LpVariable("Chairs", lowBound=0, cat="Continuous")  # x1 >= 0
x2 = LpVariable("Tables", lowBound=0, cat="Continuous")  # x2 >= 0

