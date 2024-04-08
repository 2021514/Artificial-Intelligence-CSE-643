import pandas as pd
import heapq
import math
data = pd.read_csv('Road_Distance.csv', index_col=0)
cities = data.index.tolist()

# Create a graph as an adjacency list
graph = {city: [] for city in cities}
for city in cities:
    distances = data.loc[city].to_dict()
    for dest_city, distance in distances.items():
        if dest_city != city:
            graph[city].append((dest_city, distance))
            graph[dest_city].append((city,distance))

def dijkstra(graph, start, end):
    pq = []
    heapq.heappush(pq,(0,start))
    visited = {city : False for city in graph.keys()}
    distances = {city: float('inf') for city in graph.keys()}
    distances[start]=0
    route = {city: None for city in graph.keys()}

    while pq:
        curr_dist, curr_city = heapq.heappop(pq)
        visited[curr_city]=True
        for neigbour_city,neighbour_distance in graph[curr_city]:
            new_distance = distances[curr_city] + neighbour_distance
            if distances[neigbour_city]>new_distance:
                distances[neigbour_city] = new_distance
                route[neigbour_city] = curr_city
                heapq.heappush(pq,(neighbour_distance,neigbour_city))
    Path = []
    curr_city = end
    while curr_city:
        Path.insert(0, curr_city)
        curr_city = route[curr_city]

    return Path, distances[end]
def heuristic_admissible(city, dest):
    #we use the distance to the nearest child as a heuristic
    distances = [dist for _, dist in graph[city]]
    return math.sqrt(min(distances))

def heuristic_inadmissible(city, dest):
    #we use the distance to the farthest child as a heuristic
    distances = [dist for _, dist in graph[city]]
    return max(distances)**2
a=0
def astar_admissible(graph, start, end):
    global a
    pq = []
    heapq.heappush(pq, (0 + heuristic_admissible(start, end), start))
    visited = {city: False for city in graph.keys()}
    distances = {city: float('inf') for city in graph.keys()}
    distances[start] = 0
    route = {city: None for city in graph.keys()}

    while pq:
        d, curr_city = heapq.heappop(pq)
        visited[curr_city] = True
        a+=1
        if curr_city == end:
            break

        for neighbor_city, neighbor_distance in graph[curr_city]:
            if not visited[neighbor_city]:
                new_distance = distances[curr_city] + neighbor_distance

                if new_distance < distances[neighbor_city]:
                    distances[neighbor_city] = new_distance
                    route[neighbor_city] = curr_city
                    priority = new_distance + heuristic_admissible(neighbor_city, end)
                    heapq.heappush(pq, (priority, neighbor_city))

    path = []
    curr_city = end
    while curr_city:
        path.insert(0, curr_city)
        curr_city = route[curr_city]

    return path, distances[end]
b=0
def astar_inadmissible(graph, start, end):
    global b
    pq = []
    heapq.heappush(pq, (0 + heuristic_inadmissible(start, end), start))
    visited = {city: False for city in graph.keys()}
    distances = {city: float('inf') for city in graph.keys()}
    distances[start] = 0
    route = {city: None for city in graph.keys()}

    while pq:
        d, curr_city = heapq.heappop(pq)
        visited[curr_city] = True
        b+=1
        if curr_city == end:
            break

        for neighbor_city, neighbor_distance in graph[curr_city]:
            if not visited[neighbor_city]:
                new_distance = distances[curr_city] + neighbor_distance

                if new_distance < distances[neighbor_city]:
                    distances[neighbor_city] = new_distance
                    route[neighbor_city] = curr_city
                    priority = new_distance + heuristic_inadmissible(neighbor_city, end)
                    heapq.heappush(pq, (priority, neighbor_city))

    path = []
    curr_city = end
    while curr_city:
        path.insert(0, curr_city)
        curr_city = route[curr_city]

    return path, distances[end]
def uniform_cost_search(graph, start, goal):
    pq = []
    heapq.heappush(pq, (0, start))
    costs = {city: float('inf') for city in graph.keys()}
    costs[start] = 0
    parents = {city: None for city in graph.keys()}

    while pq:
        curr_cost, curr_city = heapq.heappop(pq)

        if curr_city == goal:
            path = []
            while curr_city is not None:
                path.insert(0, curr_city)
                curr_city = parents[curr_city]
            return path, costs[goal]

        for neighbor_city, neighbor_cost in graph[curr_city]:
            new_cost = costs[curr_city] + neighbor_cost

            if costs[neighbor_city] > new_cost:
                costs[neighbor_city] = new_cost
                parents[neighbor_city] = curr_city
                heapq.heappush(pq, (new_cost, neighbor_city))

    return [],float('inf')
while (True):
    k = input("Enter source city: ")
    l = input("Enter destination city: ")
    source_city = k.capitalize()
    dest_city = l.capitalize()
    if source_city not in cities or dest_city not in cities:
        print("Source or destination city not found in the dataset.")
        break
    print("\nUsing Dijkstra:- ")
    shortest_route, shortest_distance = dijkstra(graph, source_city, dest_city)
    print(f"Shortest route from {source_city} to {dest_city}:")
    print(" → ".join(shortest_route))
    print(f"Total distance: {shortest_distance} kilometers\n")

    print("Using Uniform cost search:-")
    path, cost = uniform_cost_search(graph, source_city, dest_city)
    if path:
        print(f"Shortest path from {source_city} to {dest_city}: {' → '.join(path)}")
        print(f"Total distance: ",cost,"Kilometers\n")
    else:
        print(f"No path found from {source_city} to {dest_city}\n")
    print("Using A* Admissible:-")
    shortest_route1, shortest_distance1 = astar_admissible(graph, source_city, dest_city)
    print(f"Shortest route from {source_city} to {dest_city}:")
    print(" → ".join(shortest_route1))
    print(f"Total distance: {shortest_distance1} kilometers")
    print("Number of nodes visited: ",a,"\n")

    print("Using A* Inadmissible:-")
    shortest_route2, shortest_distance2 = astar_inadmissible(graph, source_city, dest_city)
    print(f"Shortest route from {source_city} to {dest_city}:")
    print(" → ".join(shortest_route2))
    print(f"Total distance: {shortest_distance2} kilometers")
    print("Number of nodes visited: ",b,"\n")

    n = input("Do you want to continue (Y/N): ")
    if n.lower()=='y':
        continue
    elif n.lower()=='n':
        print("Thanks for using the Application!!")
        break