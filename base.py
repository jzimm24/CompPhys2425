import numpy as np

def twoPointDist_new(x, y, dist_matrix): 
    """ input:  two points x and y - (int)
                matrix giving the distances between points - (2d array)
        return: distance (int) between point x and point y (direction x to y)
    """
    return(dist_matrix[x-1, y-1])

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
    N = len(points)
    if loop:
        dist_sum = twoPointDist(points[N-1], points[0], dist_matrix)
        for i in range(N-1):
            dist_sum += twoPointDist(points[i], points[i+1], dist_matrix)

    else:
        dist_sum = 0
        for i in range(N-1):
            dist_sum += twoPointDist(points[i], points[i+1], dist_matrix)
    return(dist_sum)

def totalTravelDist_new(path, distMat):
    N = len(path)
    sum = twoPointDist_new(path[N-1], path[0], distMat)
    for i in range(N-1):
        #print(sum)
        k = path[i]
        l = path[i+1]
        #print(k, 'to', l)
        sum += twoPointDist_new(k, l, distMat)
    return(sum)

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
        dist_sum += twoPointDist(points[i], points[i+1], distances[round(dist_sum) % periodicity,:,:])
        
    if loop:
        dist_sum += twoPointDist(points[N-1], points[0], distances[round(dist_sum) % periodicity,:,:])
    return(dist_sum)

def exchangeTwoPartsorder(x1, x2, y1, y2, arr): 
    """ input:  x1, x2, y1, y2 - positions in array at which the array is to be cut in subarrays (it needs to be x1<x2<y1<y2) - int
                array - array which is to be reordered - array
        return: reordered array (exchange the position [0,...,x1,...,x2,....,y1,...y2,...] to [0,...,y1,...,y2,....,x1,...x2,...]) - array
    """
    return(np.concatenate((arr[0:x1],arr[y1:y2+1], arr[x2+1:y1], arr[x1:x2+1], arr[y2+1:])))

def Lin_3_Opt (path): # korrigiert, funktioniert
    """ input:  path - array that is to be reordered - array
        return: reordered path (exchanges two random successive parts of the tour without altering their directions) - array
    """
    ordered_cuts = np.array([0,0,0,0])
    while ordered_cuts[1]== ordered_cuts[2]:
        
        cuts = np.random.randint(len(path), size=4) ##take for random positions in path-array and put them in array
        ordered_cuts = np.sort(cuts)                #sort the array from smallest to largest
        
    return(exchangeTwoPartsorder(ordered_cuts[0],ordered_cuts[1],ordered_cuts[2],ordered_cuts[3],path)) 
    ##ordered intput so we can use exchangeTwoParts
    
def Lin_2_Opt(path):   
    """ input:  path - array that is to be reordered - array
        return: reordered path (Lin-2-Opt move simply reverses the direction of a part of the tour ) - array
    """
    positions = np.arange(len(path)) 
    
    cut =  np.random.randint(len(path),size =2) ##take random postion in path-array
    order_cut = np.sort(cut)
    change = np.concatenate((positions[0:order_cut[0]], positions[order_cut[0]:order_cut[1]+1][::-1], positions[order_cut[1]+1:])) 
    ##make the change with the already ordered positions
    return(path[change])

def Opt_method(x,array):
    """
    Chooses method of path change
    
    input: x - = 0,1 or 2: 0: Only Lin-2, 1: Only Lin-3, 2: randomize between both
        array - array to be alterad
    output: new array with either Lin-2 or Lin-3 used upon
    """
    if x == 0:
        return Lin_2_Opt(array)
    elif x == 1:
        return Lin_3_Opt(array)
    else:
        method = np.random.choice(2) # choose if you use Lin
        if method ==1:
            return Lin_2_Opt(array)
        else:
            return Lin_3_Opt(array)
        
def traveling_MC_constDist(points, dist_matrix, tries, starting_temp = 1, alpha = 0.999, method =2):
    """ input:  points - points that should be visited by each path (in some order) - array
                dist_matrix - matrix containing the 'distances' between each point - 2darray
                tries - itterations of the Monte Carlos - Markov chain - int
                starting_temp - scalar in the exponent of the markov chain acception process - int
                alpha - scalar refgulating the decrease of the temperature after each loop iteration in the MC
                method - see Opt_method- cuurently random between Lin-2 & Lin-3
        return: points - points that should be visited by each path (in some order) - array
                pathWeights - 'distances' (better weights) of each path - array of int
                temps - temperatures after each MC step - array of int
    """
    
    pathWeights = np.zeros(tries+1)
    temps = np.zeros(tries+1)
    pathWeights[0] = totalTravelDist(points, dist_matrix)
    temps[0] = starting_temp
    cost = pathWeights[0]
    
    for i in range(tries):
        
        new_sequence = Opt_method(method,points)
        new_cost = totalTravelDist(new_sequence, dist_matrix)
        if np.random.uniform(low=0, high=1) < np.exp((pathWeights[i]-new_cost)/temps[i]):
            points = new_sequence
            cost = new_cost
        pathWeights[i+1] = cost
        temps[i+1] = alpha*temps[i] 
    return(points, pathWeights, temps)

def traveling_MC_constDist_history(points, dist_matrix, tries, starting_temp = 1, alpha = 0.999, method=2):
    """ input:  points - points that should be visited by each path (in some order) - array
                dist_matrix - matrix containing the 'distances' between each point - 2darray
                tries - itterations of the Monte Carlos - Markov chain - int
                starting_temp - scalar in the exponent of the markov chain acception process - int
                alpha - scalar regulating the decrease of the temperature after each loop iteration in the MC
                method - see Opt_method- cuurently random between Lin-2 & Lin-3
        return: pathWeights - 'distances' (better weights) of each path - array of int
                pathHistory - all paths in the order they have been explored (same as pathWeights) - 2darray
                temps - temperatures after each MC step - array of int
    """
    pathHistory = np.zeros((tries+1, len(points)))
    pathWeights = np.zeros(tries+1)
    temps = np.zeros(tries+1)
    #C = np.zeros(points+1)
    pathWeights[0] = totalTravelDist(points, dist_matrix)
    temps[0] = starting_temp
    cost = pathWeights[0]
    pathHistory[0] = points

    
    for i in range(tries):
        
        new_sequence = Opt_method(method,points)
        new_cost = totalTravelDist(new_sequence, dist_matrix)
        if np.random.uniform(low=0, high=1) < np.exp((pathWeights[i]-new_cost)/temps[i]): 
            points = new_sequence
            cost = new_cost
        pathWeights[i+1] = cost
        pathHistory[i+1] = points
        temps[i+1] = alpha*temps[i]      
    return(pathWeights, pathHistory, temps)

###now time dependent with matrices sored in dim a (3darray 3rd dim is 'the' time)
def traveling_changingDist_MC(points, distances, tries, period, starting_temp = 1, alpha = 0.999 , method =2):
    """ input:  points - points that should be visited by each path (in some order) - array
                distances - 3d-matrix containing the 'distances' and time evolution between each point - 3darray
                tries - itterations of the Monte Carlos - Markov chain - int
                period - times before repetition of matrixpattern after
                starting_temp - scalar in the exponent of the markov chain acception process - int
                alpha - scalar regulating the decrease of the temperature after each loop iteration in the MC
                method - see Opt_method- cuurently random between Lin-2 & Lin-3
        return: pathWeights - 'distances' (better weights) of each path - array of int
                pathHistory - all paths in the order they have been explored (same as pathWeights) - 2darray
                temps - temperatures after each MC step - array of int
    """
    pathHistory = np.zeros((tries+1, len(points)))
    pathWeights = np.zeros(tries+1)
    temps = np.zeros(tries+1)

    pathWeights[0] = travelWeightTotal_changingDist(points, distances, period)
    temps[0] = starting_temp
    cost = pathWeights[0]
    pathHistory[:][0] = points
 
    
    for i in range(tries):
        
        new_sequence = Opt_method(method,points)
        new_cost = travelWeightTotal_changingDist(new_sequence, distances, period)
        if np.random.uniform(low=0, high=1) < np.exp((pathWeights[i]-new_cost)/temps[i]): 
            points = new_sequence
            cost = new_cost
        pathWeights[i+1] = cost
        pathHistory[i+1] = points

        temps[i+1] = alpha*temps[i]   
    return(pathWeights, pathHistory, temps)

def traveling_MC_constDist_break(points, dist_matrix, tries, starting_temp = 1, alpha = 0.999, ameloration = -0.01,
                                 tries_stop = 100, method =2):
    """ input:  points - points that should be visited by each path (in some order) - array
                dist_matrix - matrix containing the 'distances' between each point - 2darray
                tries - itterations of the Monte Carlos - Markov chain - int
                starting_temp - scalar in the exponent of the markov chain acception process - int
                alpha - scalar refgulating the decrease of the temperature after each loop iteration in the MC
                tries_stop - check for ameloration between d[x] and d[x+tries_stop] - int
                ameloration -  Improvement requiered to stop loop
                method - see Opt_method- cuurently random between Lin-2 & Lin-3
        return: points - points that should be visited by each path (in some order) - array
                pathWeights - 'distances' (better weights) of each path - array of int
                temps - temperatures after each MC step - array of int
    """
    
    pathWeights = np.zeros(tries+1)
    temps = np.zeros(tries+1)
    pathWeights[0] = totalTravelDist(points, dist_matrix)
    temps[0] = starting_temp
    cost = pathWeights[0]
    finish = False
    for i in range(tries):
        
        if finish == False:
            new_sequence = Opt_method(method,points)
            new_cost = totalTravelDist(new_sequence, dist_matrix)
            if np.random.uniform(low=0, high=1) < np.exp((pathWeights[i]-new_cost)/temps[i]):
                points = new_sequence
                cost = new_cost
            pathWeights[i+1] = cost
            temps[i+1] = alpha*temps[i] 
            if i > tries_stop:
                counter = 0
                for z in range(tries_stop):
                    if -10**(-9) < pathWeights[i+1-z]/pathWeights[i+1]-1 < ameloration:
                        counter = counter +1
                if counter == tries_stop:
                    print('requirement met at ',i,'try')
                    finish = True
        else:
            pathWeights[i+1] = cost
            temps[i+1] = temps[i]
                
    return(points, pathWeights, temps)