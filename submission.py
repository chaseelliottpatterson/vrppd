import sys
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LoadNumber:
    def __init__(self, number, pickup, dropoff, existing_route=None):
        self.number = number
        self.pickup = pickup
        self.dropoff = dropoff
        self.dist = euclidean_distance(pickup,dropoff)
        self.existing_route = existing_route

class Route:
    def __init__(self):
        self.dist  = 0.0 
        self.path = []
        
MAX_DISTANCE = 720 #max distance constraint 12hrs converted to min
ORIGIN = Point(0,0) 

def euclidean_distance(a,b):
    return math.sqrt(math.pow(a.x-b.x,2)+math.pow(a.y-b.y,2))

def read_problem(filepath):
    load_numbers = []
    header = True
    with open(filepath) as file:
        for line in file:
            if header:
                header=False
                continue
            data = line.replace('(','').replace(')','').split(' ')
            pickup = data[1].split(',')
            dropoff = data[2].split(',')
            new_load_number = LoadNumber(int(data[0]),Point(float(pickup[0]),float(pickup[1])),Point(float(dropoff[0]),float(dropoff[1])))
            load_numbers.append(new_load_number)
    return load_numbers

def calculate_savings(load_numbers):
    #Clark-Wright step 1 calculate savings
    #S(i,j) = d(D,i)+d(D,j)-d(i,j) for every pair (i,j)
    savings_list=[]
    for i in range(len(load_numbers)):
        load_i = load_numbers[i]
        for j in range(len(load_numbers)):
            if i==j:
                continue
            load_j = load_numbers[j]

            #calculating saving for each element with formula above, then saving it to a list along with
            #  i,j this allows us to keep track of what savings correspond with which indices
            saving = euclidean_distance(load_i.dropoff,ORIGIN)+euclidean_distance(ORIGIN,load_j.pickup)-euclidean_distance(load_i.dropoff,load_j.pickup)
            savings_list.append((saving, (i,j)))

    #Clark-Wright step 2 rank the savings list in decending order of magnitude
    return sorted(savings_list, key=lambda x: x[0], reverse=True)

def route_distances(stops):
    dist = euclidean_distance(ORIGIN,stops[0].pickup)+euclidean_distance(stops[-1].dropoff,ORIGIN) #always will have to add initial and final locaitons
    for idx in range(len(stops)):
        dist = dist + stops[idx].dist
        if idx < (len(stops)-1):
            dist = dist + euclidean_distance(stops[idx].dropoff, stops[idx+1].pickup)
    return dist

def build_routes(sorted_savings, load_numbers):
    routes = []
    #Clark-Wright step 3 
    #For the savings S(i,j) under consideration, include link (i,j) in a route if no route constraints will be violated through the inclusion of (i,j) in a route, and if:
    for saving in sorted_savings:
        load_i_index = saving[1][0]
        load_j_index = saving[1][1]
        load_i = load_numbers[load_i_index]
        load_j = load_numbers[load_j_index]

        #a. Either, neither i nor j have already been assigned to a route, in which case a new route is initiated including both i and j.
        if load_i.existing_route is None and load_j.existing_route is None:
                #if route does not exceed max distance create a new route from the 2 loads
                length = euclidean_distance(ORIGIN,load_i.pickup) + load_i.dist + euclidean_distance(load_i.dropoff, load_j.pickup) + load_j.dist + euclidean_distance(load_j.dropoff, ORIGIN)
                if length <= MAX_DISTANCE:
                    new_route = Route()
                    new_route.dist = length
                    new_route.path = [load_i, load_j]
                    load_i.existing_route=new_route
                    load_j.existing_route=new_route
                    routes.append(new_route)

        #b. Or, exactly one of the two points (i or j) has already been included in an existing route and that point is not interior to that route 
        # (a point is interior to a route if it is not adjacent to the depot D in the order of traversal of points), in which case the link (i, j) is added to that same route. 
        elif load_i.existing_route is not None and load_j.existing_route is None:   #i exists j doesn't case
            my_route = load_i.existing_route
            idx = my_route.path.index(load_i)
            if idx == 0:                                                            #check if this is fitst stop in route
                if route_distances([load_j] + my_route.path) <= MAX_DISTANCE:       #if it is fitst stop and adding it doesnt exceed max distance go ahead and add it to the start
                    load_j.existing_route = my_route
                    my_route.path = [load_j] + my_route.path
            elif idx == len(my_route.path) - 1:                                     #check if this is last stop in route
                if route_distances(my_route.path+[load_j]) <= MAX_DISTANCE:         #if it is last stop and adding it doesnt exceed max distance go ahead and add it to the end
                    load_j.existing_route = my_route
                    my_route.path.append(load_j)

        elif load_i.existing_route is None and load_j.existing_route is not None:   #j exists i doesn't case
            my_route = load_j.existing_route
            jdx = my_route.path.index(load_j)
            if jdx == 0:                                                            #check if this is fitst stop in route
                if route_distances([load_i] + my_route.path) <= MAX_DISTANCE:       #if it is fitst stop and adding it doesnt exceed max distance go ahead and add it to the start
                    load_i.existing_route = my_route
                    my_route.path = [load_i] + my_route.path
            elif jdx == len(my_route.path) - 1:                                     #check if this is last stop in route
                if route_distances(my_route.path+[load_i]) <= MAX_DISTANCE:         #if it is last stop and adding it doesnt exceed max distance go ahead and add it to the end
                    load_i.existing_route = my_route
                    my_route.path.append(load_i)

        #c. Or, both i and j have already been included in two different existing routes and neither point is interior to its route, in which case the two routes are merged. 
        else:
            route_i = load_i.existing_route
            route_j = load_j.existing_route
            idx = route_i.path.index(load_i)
            jdx = route_j.path.index(load_j)
            if idx == len(route_i.path)-1 and (jdx == 0) and (route_i != route_j):
                if MAX_DISTANCE >= route_distances(route_i.path+route_j.path):
                    route_i.path = route_i.path+route_j.path
                    for load_number in route_j.path:
                        load_number.existing_route = route_i
                    routes.remove(route_j)

            #Clark-Wright step 4
            #If the savings list s(i, j) has not been exhausted, return to Step 3, processing the next entry in the list; otherwise, stop: the solution to the VRP consists of the routes created during
            #  Step 3.(Any points that have not been assigned to a route during Step 3 must each be served by a vehicle route that begins at the depot D visits the unassigned point and returns to D.)
            for unassigned_load in load_numbers:
                if unassigned_load.existing_route is None:
                    unassigned_route = Route()
                    unassigned_route.path.append(unassigned_load)
                    unassigned_load.existing_route=unassigned_route
                    routes.append(unassigned_route)
    return routes
    


def main():
    if len(sys.argv)>1:
        filepath = sys.argv[1]
    load_numbers = read_problem(filepath)
    sorted_savings = calculate_savings(load_numbers)
    routes = build_routes(sorted_savings,load_numbers)
    print(len(routes))
    
if __name__ == "__main__":
    main()