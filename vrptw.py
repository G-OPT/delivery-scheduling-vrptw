import math
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2, pywrapcp

# -----------------------------------------
# Load CSV Data
# -----------------------------------------
df = pd.read_csv("delivery_vrptw.csv")

loc_names = df["location"].tolist()
lats = df["lat"].tolist()
lons = df["lon"].tolist()
time_windows = list(zip(df["tw_start"], df["tw_end"]))
num_nodes = len(df)

# -----------------------------------------
# Distance → Time Matrix (Haversine + 30 km/h speed)
# -----------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# Travel time matrix (min)
time_matrix = []
for i in range(num_nodes):
    row = []
    for j in range(num_nodes):
        d = haversine(lats[i], lons[i], lats[j], lons[j])
        t = int(round((d / 30) * 60))  # 30 km/h → minutes
        row.append(t)
    time_matrix.append(row)

num_vehicles = 2
depot = 0

# -----------------------------------------
# Routing Model
# -----------------------------------------
manager = pywrapcp.RoutingIndexManager(num_nodes, num_vehicles, depot)
routing = pywrapcp.RoutingModel(manager)

# Travel callback
def time_callback(from_index, to_index):
    f = manager.IndexToNode(from_index)
    t = manager.IndexToNode(to_index)
    return time_matrix[f][t]

transit_callback_index = routing.RegisterTransitCallback(time_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# -----------------------------------------
# Time Window Dimension
# -----------------------------------------
routing.AddDimension(
    transit_callback_index,
    30,     # waiting allowed
    120,    # max route duration
    False,
    "Time"
)

time_dim = routing.GetDimensionOrDie("Time")

# Apply windows
for i, (tw_start, tw_end) in enumerate(time_windows):
    index = manager.NodeToIndex(i)
    time_dim.CumulVar(index).SetRange(tw_start, tw_end)

# Vehicle start times
for v in range(num_vehicles):
    start = routing.Start(v)
    time_dim.CumulVar(start).SetRange(0, 120)

# -----------------------------------------
# Search Parameters
# -----------------------------------------
params = pywrapcp.DefaultRoutingSearchParameters()
params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
params.time_limit.seconds = 3

solution = routing.SolveWithParameters(params)

# -----------------------------------------
# Print Solution
# -----------------------------------------
if solution:
    for v in range(num_vehicles):
        index = routing.Start(v)
        print(f"\nRoute for vehicle {v}:")

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            tvar = time_dim.CumulVar(index)
            arr = solution.Value(tvar)
            print(f" {loc_names[node]} (arrive={arr}) -> ", end="")
            index = solution.Value(routing.NextVar(index))

        node = manager.IndexToNode(index)
        tvar = time_dim.CumulVar(index)
        arr = solution.Value(tvar)
        print(f"{loc_names[node]} (arrive={arr})\n")

else:
    print("No solution found.")
