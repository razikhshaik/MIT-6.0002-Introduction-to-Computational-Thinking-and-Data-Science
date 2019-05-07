###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cow_dict = {}
    with open(filename, 'r') as f:
         for i in f.readlines():
             cow_name, cow_weight = i.split(',')
             cow_dict[cow_name] = int(cow_weight)
    return cow_dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    transport_cow = cows.copy()
    num_trips = 0
    limitper_trip = limit
    tripsummary = []
    while len(transport_cow) > 0:
        current_trip = []
        limitper_trip = limit
        x = sorted(transport_cow, key=(lambda key:transport_cow[key]), reverse=True)
        for c in x:
            if limitper_trip >= transport_cow[c]:
                current_trip.append(c)
                limitper_trip -= transport_cow[c]
                del transport_cow[c]
            if limitper_trip <= 0:
                break
        tripsummary.append(current_trip)
        num_trips += 1
    return tripsummary
            



# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    transport_cow = cows.copy()
    num_trips = 0
    limitper_trip = limit
    tripsummary = []
    # while len(transport_cow) > 0:
    #     current_trip, left_overs, con, weight_left = compute_tree([], transport_cow)
    #     transport_cow = left_overs.copy()
    #     transport_cow = {**left_overs, **con}
    #     tripsummary.append(current_trip)
    #     num_trips += 1
    # return tripsummary
    combinations = list(get_partitions(transport_cow))
    #print(len(combinations))

    flag = True
    legal = []
    trip_lengths = []
    for comb in combinations:
        # all trips
        num_trips = 0
        for trip in comb:
            load = 0
            for c in trip:
                load += cows[c]
            num_trips += 1
            if load > limit:
                # discard this combination
                flag = False
        if flag:
            legal.append(comb)
            trip_lengths.append(num_trips)
        else:
            flag = True
    index = trip_lengths.index(min(trip_lengths))
    return legal[index]




# this optimizes foor just one trip
def compute_tree(trip, left_over_cows_dict, considered_but_not_added = {}, limit = 10):
    trip = trip.copy()
    left_over_cows_dict = left_over_cows_dict.copy()
    considered_but_not_added = considered_but_not_added.copy()
    con = considered_but_not_added.copy()
    if len(left_over_cows_dict) == 0:
        return (trip, {}, considered_but_not_added, limit)
    if limit == 0:
        return (trip, left_over_cows_dict, considered_but_not_added, limit)
    cows = list(left_over_cows_dict.keys())
    d = left_over_cows_dict.copy()
    first_cow, weight = cows[0], left_over_cows_dict[cows[0]]
    del d[first_cow]
    con[first_cow] = weight
    without_first_cow = compute_tree(trip, d, con, limit)
    with_first_cow = None
    if limit >= weight:
        trip.append(first_cow)
        with_first_cow = compute_tree(trip, d, considered_but_not_added, limit-weight)
    if with_first_cow != None:
        if without_first_cow[3] >= with_first_cow[3]:
            return with_first_cow
        else:
            return without_first_cow
    else:
        return without_first_cow
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows("ps1\ps1_cow_data.txt")
    start = time.time()
    trip = greedy_cow_transport(cows)
    timedend = time.time()
    print("Time taken for greedy:", (timedend- start))
    print("num of trips:", len(trip))
    load_carried = []
    for i in trip:
        load = 0
        for c in i:
            load += cows[c]
        load_carried.append(load)
    print("avg load carried per trip:", float(sum(load_carried))/float(len(load_carried)))

    start = time.time()
    trip = brute_force_cow_transport(cows)
    timedend = time.time()
    print("Time taken fpr brute force:", (timedend- start))
    print("num of trips:", len(trip))
    load_carried = []
    for i in trip:
        load = 0
        for c in i:
            load += cows[c]
        load_carried.append(load)
    print("avg load carried per trip:", float(sum(load_carried))/float(len(load_carried)))


if __name__ == "__main__":
    cows = load_cows("ps1\ps1_cow_data.txt")
    trip = greedy_cow_transport(cows)
    print(trip)
    #print(compute_tree([], cows))
    print(brute_force_cow_transport(cows))
    compare_cow_transport_algorithms()