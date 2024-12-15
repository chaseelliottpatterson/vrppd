import sys
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LoadNumber:
    def __init__(self, number, pickup, dropoff):
        self.number = number
        self.pickup = pickup
        self.dropoff = dropoff
        self.dist = euclidean_distance(pickup,dropoff)
        
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

## ToDo

    #Clark-Wright step 3 
    #For the savings S(i,j) under consideration, include link (i,j) in a route if no route constraints will be violated through the inclusion of (i,j) in a route, and if:
        #
        #a. Either, neither i nor j have already been assigned to a route, in which case a new route is initiated including both i and j.
        #
        #b. Or, exactly one of the two points (i or j) has already been included in an existing route and that point is not interior to that route 
        # (a point is interior to a route if it is not adjacent to the depot D in the order of traversal of points), in which case the link (i, j) is added to that same route.      
        #
        #c. Or, both i and j have already been included in two different existing routes and neither point is interior to its route, in which case the two routes are merged.
    
    #Clark-Wright step 4
    #If the savings list s(i, j) has not been exhausted, return to Step 3, processing the next entry in the list; otherwise, stop: the solution to the VRP consists of the routes created during
    #  Step 3.(Any points that have not been assigned to a route during Step 3 must each be served by a vehicle route that begins at the depot D visits the unassigned point and returns to D.)


def main():
    if len(sys.argv)>1:
        filepath = sys.argv[1]
    load_numbers = read_problem(filepath)
    sorted_savings = calculate_savings(load_numbers)
    print(sorted_savings)
if __name__ == "__main__":
    main()