import numpy as np
#import matplotlib.pyplot as plt

##TODO: -Code not yet tested...
##      -write function that searches for least weighted path by comparing every single permutation (see C++ code)
##      -test Lin_2_Opt_fast
###     -merge functions and give option flags for different outputs and memories instead

def twoPointDist(x, y, dist_matrix):
    """ input:  two points x and y - (int)
                matrix giving the distances between points - (2d array)
        return: distance (int) between point x and point y (direction x to y)
    """
    return(dist_matrix[x, y])

def totalTravelDist(points, dist_matrix, loop=True):
    """ input:  points - array of points that gives the path - array
                dist_matrix - matrix containing the distances between all points (in both directions) - 2d array
                loop - info if the path needs to be a loop (start position = end position) - boolean
        output: dist_sum - total weight of the given path - int
    """
    if loop:
        N = len(points)
        dist_sum = twoPointDist(points[N], points[0], dist_matrix)
        for i in range(N-1):
            dist_sum += twoPointDist(points[i], points[i+1], dist_matrix)

    else:
        dist_sum = 0
        for i in range(N-1):
            dist_sum += twoPointDist(points[i], points[i+1], dist_matrix)
    return(dist_sum)

def travelWeightTotal_changingDist(points, distances, periodicity, loop = True):
    """ input:  points - array of points representing the path - array
                distances - matrices containing the distances between all points (in both directions) at different 'times' (3rd dim = time dim) - 3d array
                periodicity - periodicity of the time matrices in time - int
                loop - info if the path needs to be a loop (start position = end position) - boolean
        return: dist_sum - total weight of the given path - int
    """
    N = len(points)
    dist_sum = 0
    for i in range(N-1):
        dist_sum += twoPointDist(points[i], points[i+1], distances[:][:][dist_sum % periodicity])
    if loop:
        dist_sum += twoPointDist(points[N], points[0], distances[:][:][dist_sum % periodicity])
    return(dist_sum)

def exchange_two_parts(x1,x2,y1,y2,array): 
    """ exchange the position [0,...,x1,...,x2,....,y1,...y2,...] to [0,...,y1,...,y2,....,x1,...x2,...]
        or vice-versa. x1 = x2 or y1 =y2 are possible
    """
    if x1 < y1:
        if x1 > 0:
            change = np.concatenate((array[0:x1],array[y1:y2+1], array[x2+1:y1], array[x1:x2+1], array[y2+1:]))
        else:
            change = np.concatenate((array[y1:y2+1], array[x2+1:y1], array[x1:x2+1], array[y2+1:]))
    else:
        if y1 > 0:
            change = np.concatenate((array[0:y1],array[x1:x2+1], array[y2+1:x1], array[y1:y2+1], array[x2+1:]))
        else:
            change = np.concatenate((array[x1:x2+1], array[y2+1:x1], array[y1:y2+1], array[x2+1:]))
    return(change)

##the following function should be enough in any case that provides ordered x1, x2, y1, y2 (smallest to largest)
def exchangeTwoPartsFast(x1, x2, y1, y2, arr):
    """ input:  x1, x2, y1, y2 - positions in array at which the array is to be cut in subarrays (it needs to be x1<x2<y1<y2) - int
                array - array which is to be reordered - array
        return: reordered array (exchange the position [0,...,x1,...,x2,....,y1,...y2,...] to [0,...,y1,...,y2,....,x1,...x2,...]) - array
    """
    return(np.concatenate((arr[0:x1],arr[y1:y2+1], arr[x2+1:y1], arr[x1:x2+1], arr[y2+1:])))

def Lin_3_Opt (way): ###yoooooooooo wieso heißt das Lin 3 Opt? Check ich den Namen einfach nicht?
    """
    Lin-3-Opt  exchanges two random successive parts of the tour without altering their directions.
    """
    candidates =np.array([])
    while len(candidates)==0:
        a1 = np.random.randint(len(way))
        a2 = np.random.randint(len(way))
        positions = np.arange(len(way))
        if a1 < a2:
            x1 = a1
            x2 = a2
        else:
            x1 = a2
            x2 = a1

        ind = (positions < x1) | (positions > x2)
        candidates = positions[ind]

    b1 = int(np.random.choice(candidates))
    
    if b1 < x1:
        b2 = int(np.random.choice(positions[:x1]))
    else: 
        b2 = int( np.random.choice(positions[x2+1:]))
        
    if b1 < b2:
            y1 = b1
            y2 = b2
    else:
            y1 = b2
            y2 = b1

    return way[exchange_two_parts(x1,x2,y1,y2,positions)]

def Lin_3_Opt_fast (path):
    """ input:  path - array that is to be reordered - array
        return: reordered path (exchanges two random successive parts of the tour without altering their directions) - array
    """

    cuts = np.random.randint(len(path), size=4) ##take for random positions in path-array and put them in array
    ordered_cuts = np.sort(cuts)                #sort the array from smallest to largest

    return(exchangeTwoPartsFast(ordered_cuts[0],ordered_cuts[1],ordered_cuts[2],ordered_cuts[3],path)) ##ordered intput so we can use exchangeTwoPartsFast

def Lin_2_Opt(way):
    """
    Lin-2-Opt move simply reverses the direction of a
    part of the tour  
    """
    a1 = 0
    a2 = 0
    while a1==a2:
        a1 = np.random.randint(len(way))
        a2 = np.random.randint(len(way))
    positions = np.arange(len(way)) 
    if a1 < a2:
        x1 = a1
        x2 = a2
    else:
        x1 = a2
        x2 = a1
    change = np.concatenate((positions[0:x1], positions[x1:x2+1][::-1], positions[x2+1:]))
    return way[change]

def Lin_2_Opt_fast(path):   ##!!!!!!!!!!!!!!!!!!!!does this work this way or does this produce lower positions more frequently? !!!!!!!!!!!!!!!!!!!!1
    """ input:  path - array that is to be reordered - array
        return: reordered path (Lin-2-Opt move simply reverses the direction of a part of the tour ) - array
    """
    positions = np.arange(len(path)) 
    x2 = np.random.randint(len(path)) ##take random postion in path-array
    x1 = np.random.randint(x2)  ##take random postion lower than previously selected position
    change = np.concatenate((positions[0:x1], positions[x1:x2+1][::-1], positions[x2+1:])) ##make the change with the already ordered positions
    return(path[change])

def traveling_Yann(points, matrix, steps, T=1, alpha = 1):
    """
    Time independent traveling salesman with toggable temperature and temperature reduction (0.8<alpha<0.999)
    """
    
    cost = np.zeros(steps+1)
    temp = np.zeros(steps+1)
    C = np.zeros(steps+1)
    start = points
    summ = totalTravelDist(start, matrix)
    cost[0] = summ
    temp[0] = T
    C[0] = np.var(cost)/T**2
    
    for tries in range(steps):
        
        method = np.random.choice(2) # choose if you use Lin
        if method ==1:
            new_start = Lin_2_Opt(start)
        else:
            new_start = Lin_3_Opt(start)
        new_sum = totalTravelDist(new_start, matrix)
        if np.random.uniform(low=0, high=1) < np.exp((summ-new_sum)/T):
            start = new_start
            summ = totalTravelDist(new_start, matrix)
        cost[tries+1] = summ
        C[tries+1] = np.var(cost)/T**2
        temp[tries+1] = T
        T = alpha*T     
    return start, summ, cost, temp, C


### Time independent traveling salesman with toggable temperature and temperature reduction (0.8<alpha<0.999)
##  If we really want to trim it down and make it more storage efficient we could only get the best path and best weight as output
def traveling_MC_constDist_Julius(points, dist_matrix, tries, starting_temp = 1, alpha = 1):
    """ input:  points - points that should be visited by each path (in some order) - array
                dist_matrix - matrix containing the 'distances' between each point - 2darray
                tries - itterations of the Monte Carlos - Markov chain - int
                starting_temp - scalar in the exponent of the markov chain acception process - int
                alpha - scalar refgulating the decrease of the temperature after each loop iteration in the MC
        return: points - points that should be visited by each path (in some order) - array
                pathWeights - 'distances' (better weights) of each path - array of int
                temps - temperatures after each MC step - array of int
    """
    
    pathWeights = np.zeros(points+1)
    temps = np.zeros(points+1)
    #C = np.zeros(points+1)     ##What is this? Warum ist diese Groesse fuer uns von Bedeutung?
    pathWeights[0] = totalTravelDist(points, dist_matrix)
    temps[0] = starting_temp
    cost = pathWeights[0]
    #C[0] = np.var(pathWeights)/T**2 ##What is this? Warum ist diese Groesse fuer uns von Bedeutung?
    
    for i in range(tries):
        
        new_sequence = Lin_3_Opt(points)
        new_cost = totalTravelDist(new_sequence, dist_matrix)
        if np.random.uniform(low=0, high=1) < np.exp((pathWeights[i]-new_cost)/temps[i]):
            points = new_sequence
            cost = new_cost
        pathWeights[i+1] = cost
        #C[i+1] = np.var(cost)/T**2
        temps[i+1] = T
        T = alpha*T     
    return(points, pathWeights, temps) 

def traveling_MC_constDist_history_Julius(points, dist_matrix, tries, starting_temp = 1, alpha = 1):
    """ input:  points - points that should be visited by each path (in some order) - array
                dist_matrix - matrix containing the 'distances' between each point - 2darray
                tries - itterations of the Monte Carlos - Markov chain - int
                starting_temp - scalar in the exponent of the markov chain acception process - int
                alpha - scalar refgulating the decrease of the temperature after each loop iteration in the MC
        return: pathWeights - 'distances' (better weights) of each path - array of int
                pathHistory - all paths in the order they have been explored (same as pathWeights) - 2darray
                temps - temperatures after each MC step - array of int
    """
    pathHistory = np.zeros((points, tries+1))
    pathWeights = np.zeros(points+1)
    temps = np.zeros(points+1)
    #C = np.zeros(points+1)
    pathWeights[0] = totalTravelDist(points, dist_matrix)
    temps[0] = starting_temp
    cost = pathWeights[0]
    pathHistory[:][0] = points
    #C[0] = np.var(pathWeights)/T**2 ##What is this? Warum ist diese Groesse fuer uns von Bedeutung?
    
    for i in range(tries):
        
        new_sequence = Lin_3_Opt(points)
        new_cost = totalTravelDist(new_sequence, dist_matrix)
        if np.random.uniform(low=0, high=1) < np.exp((pathWeights[i]-new_cost)/temps[i]): ##should it be temps[i+1]?????
            points = new_sequence
            cost = new_cost
        pathWeights[i+1] = cost
        pathHistory[i+1] = points
        #C[tries+1] = np.var(cost)/T**2
        temps[i+1] = T
        T = alpha*T     
    return(pathWeights, pathHistory, temps)

###now time dependent with matrices sored in dim a (3darray 3rd dim is 'the' time)
def traveling_changingDist_MC(points, distances, tries, starting_temp = 1, alpha = 1, period):
    """
    Time dependent traveling salesman with toggable temperature and temperature reduction (0.8<alpha<0.999)
    """
    pathHistory = np.zeros((points, tries+1))
    pathWeights = np.zeros(points+1)
    temps = np.zeros(points+1)
    #C = np.zeros(points+1)
    pathWeights[0] = travelWeightTotal_changingDist(points, distances, period)
    temps[0] = starting_temp
    cost = pathWeights[0]
    pathHistory[:][0] = points
    #C[0] = np.var(pathWeights)/T**2 ##What is this? Warum ist diese Groesse fuer uns von Bedeutung?
    
    for i in range(tries):
        
        new_sequence = Lin_3_Opt(points)
        new_cost = travelWeightTotal_changingDist(new_sequence, distances, period)
        if np.random.uniform(low=0, high=1) < np.exp((pathWeights[i]-new_cost)/temps[i]): ##should it be temps[i+1]?????
            points = new_sequence
            cost = new_cost
        pathWeights[i+1] = cost
        pathHistory[i+1] = points
        #C[tries+1] = np.var(cost)/T**2
        temps[i+1] = T
        T = alpha*T     
    return(pathWeights, pathHistory, temps)

