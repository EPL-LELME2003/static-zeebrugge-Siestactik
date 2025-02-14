import pyomo.environ as pyo

# Create a Pyomo model
model = pyo.ConcreteModel()

# Define model parameters
V_per_boat = 200000 #[m³]
LHV_NH3 = 18.5 * 10**6 #[J/kg]
rho_NH3 = 600 #[kg/m³]
eta_NH3 = 0.47
hydrogen_per_NH3 = 0.18 * 10**3 #[kg_H2/kg_NH3]
LHV_CH4 = 50 * 10**6 #[J/kg]
rho_CH4 = 500 #[kg/m³]
eta_CH4 = 0.35
hydrogen_per_CH4 = 0.25 * 10**3 #[kg_H2/kg_CH4]
CO2_per_CH4 = 2.75 #[kg_CO2/kg_CH4]

# Define model variables
model.b1 = pyo.Var(within=pyo.NonNegativeIntegers, bounds=(0, 100))
model.b2 = pyo.Var(within=pyo.NonNegativeIntegers, bounds=(0, 100))

# Define the objective functions
model.hydrogen = pyo.Objective(expr=model.b1*V_per_boat*rho_CH4*hydrogen_per_CH4+model.b2*V_per_boat*rho_NH3*hydrogen_per_NH3, sense=pyo.maximize)

# Define the constraints
model.max_capa = pyo.Constraint(expr=model.b1+model.b2<=100)
model.carbon_limit = pyo.Constraint(expr=model.b1*V_per_boat*rho_CH4*CO2_per_CH4<=14*10**6)
model.energy_limit = pyo.Constraint(expr=model.b1*V_per_boat*rho_CH4*LHV_CH4/eta_CH4+model.b2*V_per_boat*rho_NH3*LHV_NH3/eta_NH3<=(140*3600)*10**12)

# Specify the path towards your solver (gurobi) file
solver = pyo.SolverFactory('\gurobi1201\win64\gurobi.lic')
sol = solver.solve(model)

# Print here the number of CH4 boats and NH3 boats
print(f'Nombre de bateau CH4 : {model.b1}')
print(f'Nombre de bateau NH3 : {model.b2}')
