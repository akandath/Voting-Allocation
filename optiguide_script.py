import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd


# Loading Dataset
data = pd.read_csv('2026_full_data.csv')

time_periods = data.columns[26:].values
num_time_periods = len(time_periods)
precinct_num = data.shape[0]
clusters = data['cluster'].values
cluster_dict = {0: 3, 1: 5, 2: 3, 3: 5, 4: 5, 5: 3}
arrival_rates = data.iloc[:, 26:].values  # Shape: [precinct_num][num_time_periods]

# Service rates
service_rate_check_in = 30 / 12  # 2.5 voters per 5-minute period
service_rate_voting = 60 / 12  # 5 voters per 5-minute period

# Resource limits
total_check_in_stations = precinct_num * 3
total_voting_booths = precinct_num * 9
max_check_in_stations = 5
max_voting_booths = 10

# Create a new model
m = gp.Model("MinimizeQueueWaiting")

# OPTIGUIDE DATA CODE GOES HERE

C = m.addVars(precinct_num, vtype=GRB.INTEGER, lb=1, ub=max_check_in_stations, name="CheckInStations")
V = m.addVars(precinct_num, vtype=GRB.INTEGER, lb=3, ub=max_voting_booths, name="VotingBooths")
W_checkin = m.addVars(precinct_num, num_time_periods, vtype=GRB.INTEGER, lb=0, name="CheckInQueue")
W_voting = m.addVars(precinct_num, num_time_periods, vtype=GRB.INTEGER, lb=0, name="VotingQueue")

# Queue constraints
for i in range(precinct_num):
    service_capacity = C[i] * service_rate_check_in
    m.addConstr(W_checkin[i, 0] >= arrival_rates[i, 0] - service_capacity,name=f"InitialQueue_{i}")
    m.addConstr(W_checkin[i, 0] >= 0,name=f"NonNegativeQueue_{i}_0")
    m.addConstr(W_voting[i, 0] >= 0,name=f"NonNegativeVotingQueue_{i}")
    min_booth_voting = cluster_dict[clusters[i]]
    m.addConstr(V[i] >= min_booth_voting,name=f"MinVotingBooths_{i}")



# OPTIGUIDE CONSTRAINT CODE GOES HERE
# Add dynamic queue constraints
for i in range(precinct_num):
    for t in range(1, num_time_periods):
        service_capacity_checkin = C[i] * service_rate_check_in
        m.addConstr(W_checkin[i, t] >= W_checkin[i, t-1] + arrival_rates[i, t] - service_capacity_checkin,name=f"QueueDynamics_{i}_{t}")
        m.addConstr(W_checkin[i, t] >= 0,name=f"NonNegativeQueue_{i}_{t}")
        service_capacity_voting = V[i] * service_rate_voting
        m.addConstr(W_voting[i, t] >= W_voting[i, t-1] + W_checkin[i, t-1] - service_capacity_voting,name=f"VotingQueueDynamics_{i}_{t}")
        m.addConstr(W_voting[i, t] >= 0,name=f"NonNegativeVotingQueue_{i}_{t}")


# Constraints for total resource limits
m.addConstr(gp.quicksum(C[i] for i in range(precinct_num)) <= total_check_in_stations,name="TotalCheckInStations")
m.addConstr(gp.quicksum(V[i] for i in range(precinct_num)) <= total_voting_booths,name="TotalVotingBooths")

# Objective function: Minimize total queue lengths
m.setObjective(gp.quicksum(W_checkin[i, t] for i in range(precinct_num) for t in range(num_time_periods)) +gp.quicksum(W_voting[i, t] for i in range(precinct_num) for t in range(num_time_periods)),GRB.MINIMIZE)

# Solve the model
m.setParam('OutputFlag', 1)
m.setParam('MIPGap', 0.06)
m.optimize()

# Display results
prec = []
check_in = []
voting = []
checkin_stations = []
voting_stations = []

if m.status == GRB.OPTIMAL:
    print("Optimal solution found!")
    for i in range(precinct_num):
        prec.append(i)
        check_in_val = int(C[i].x)
        voting_val = int(V[i].x)
        queue_sizes_checkin = [W_checkin[i, t].x for t in range(num_time_periods)]
        queue_sizes_voting = [W_voting[i, t].x for t in range(num_time_periods)]
        check_in.append(sum(queue_sizes_checkin))
        voting.append(sum(queue_sizes_voting))
        checkin_stations.append(check_in_val)
        voting_stations.append(voting_val)
else:
    print("No optimal solution found. Status code:", m.status)
    if m.status == GRB.INFEASIBLE:
        print("Model is infeasible. Computing IIS (Irreducible Inconsistent Subsystem)...")
        m.computeIIS()
        m.write("model.ilp")
        print("IIS written to 'model.ilp'")

print(f"Objective value: {m.objVal}")