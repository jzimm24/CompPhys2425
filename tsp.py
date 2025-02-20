import numpy as np
import base

def Nearest_Neighbor(points,distance,start):
    """
        Calculate way with minial distance through Nearest_Neighbor algorithm with given start point
        Input: points - points of interests - integer array from 0-#cities-1
               distances - 2d-matrix containing the distances
               start- startpoint - integer
        Output: way with minimal_distances- by Nearest_Neighbor algorithm
    
    """
    way = np.array([start]) # start with startpoint
    
    while len(way) != len(points):
        min_dist = np.max(distance)+1
        
        for  i in range(len(points)):
            
            if (distance[way[-1],i] < min_dist) and (i not in way):
                # minimal distance and not yet visited city
                min_dist = distance[way[-1],i]
                new_point = i
        way = np.append(way,new_point)
        
    way = np.append(way,start) # end with startpoint
    return way   

def Nearest_Neighbor_all_start(points,distance):
    """
        Calculate way with minial distance through Nearest_Neighbor algorithm
        Input: points - points of interests - integer array from 0-#cities-1
               distances - 2d-matrix containing the distances
        Output: way with minimal_distances- by Nearest_Neighbor algorithm
                minimal_distance
    
    """
    way = points
    min_dist = base.totalTravelDist(points,distance)
    for j in range(len(points)): # go through all points
        new_way = Nearest_Neighbor(points,distance,j)
        new_dist = base.totalTravelDist(new_way,distance)
        if new_dist < min_dist:
            min_dist = new_dist
            way = new_way
    return (way,min_dist)

def Double_side_Nearest_Neighbor(points,distance,start):
    """
        Calculate way with minial distance through Double_side_Nearest_Neighbor algorithm with given start point:
        nearest neighbour from left and right.
        Input: points - points of interests - integer array from 0-#cities-1
               distances - 2d-matrix containing the distances
               start- startpoint - integer
        Output: way with minimal_distances- by Double_side_Nearest_Neighbor algorithm
    
    """
    way_right = np.array([start]) # start with startpoint
    way_left = np.array([start])
    used = np.array([start]) # used 
    while (len(way_right)+len(way_left)-1) < len(points):
        min_dist = np.max(distance)+1
        
        for  i in range(len(points)):
            
            if (distance[way_right[-1],i] < min_dist) and (i not in used):
                # minimal distance and not yet visited city
                min_dist = distance[way_right[-1],i]
                new_point = i
        way_right = np.append(way_right,new_point)
        used = np.append(used,new_point)
        min_dist = np.max(distance)+1
        if len(used) != len(points):
            for  i in range(len(points)):
                if (distance[way_left[0],i] < min_dist) and (i not in used):
                    # minimal distance and not yet visited city
                    min_dist = distance[way_left[0],i]
                    new_point = i
            way_left = np.append(new_point,way_left)
            used = np.append(used,new_point)
    way = np.append(way_right,way_left) # end with startpoint
    return way   

def Double_side_Nearest_Neighbor_all_start(points,distance):
    """
        Calculate way with minial distance through Double_side_Nearest_Neighbor algorithm
        Input: points - points of interests - integer array from 0-#cities-1
               distances - 2d-matrix containing the distances
        Output: way with minimal_distances- by Nearest_Neighbor algorithm
                minimal_distance
    
    """
    way = points
    min_dist = base.totalTravelDist(points,distance)
    for j in range(len(points)): # go through all points
        new_way = Double_side_Nearest_Neighbor(points,distance,j)
        new_dist = base.totalTravelDist(new_way,distance)
        if new_dist < min_dist:
            min_dist = new_dist
            way = new_way
    return (way,min_dist)

def average_dist(distance):
    """
        Pre-processing of the distance Matrix to see wich matrix is in average farther away
        Input: distance 2d-matrix
        Output: Distance matrix, which priotize matrices, which are further away
    """
    
    N = len(distance)
    A = np.zeros((N,N))
    x = np.zeros(N)
    for i in range(N):
        x[i] = np.mean(distance[i,:])
    min_dist_points = np.min(x) 
    max_dist_points = np.max(x)
    average_dist = (max_dist_points + min_dist_points)/2
    for i in range(N):
        if (x[i] > average_dist):
            x[i] = average_dist- (x[i] - average_dist);
        else:
            x[i]=average_dist + (average_dist - x[i] )
    for i in range(N):
        for j in range(N): 
            A[i][j]=((N*distance[i][j])+ x[j])/2;
    return A

def nearest_Insertion(distance):
    """
        Implementation of nearest Insertion method: inserting nodes to cycle, so that length increase is minimal
        Input: distance 2d-matrix
        Output: samllest path regarding nearest Insertion method
    
    """
    
    N = len(distance)
    points = np.arange(N)
    x = np.random.choice(points, size=1, replace=False)
    minn = np.max(distance)
    for i in range(len(points)):
        if i!=x:
            if distance[i,x]<minn:
                minn = distance[i,x]
                y =i
    cycle = np.append(x,y)
    while len(cycle) <N:
        d = np.max(distance)
        for c in range(len(cycle)-1):
            pos1 = cycle[c]
            pos2 = cycle[c+1]
            for j in range(N):
                if j not in cycle:
                    if distance[pos1,j]+distance[j,pos2]-distance[pos1,pos2] <d:
                        d = distance[pos1,j]+distance[j,pos2]-distance[pos1,pos2] 
                        k = j
                        rep_c = c+1
        cycle = np.insert(cycle,rep_c,k)
        

    cycle = np.append(cycle,cycle[0])
    return cycle
            
def prim(distance):
    """Calculate minimal spanning tree through prim algorihm:
       Always add edge to a new vertex with smallest value to existing tree
       Input: distance_ matrix containing distance to all the points
       Output: E_ edges connecting the tree in one array
               E_plot _  dges connecting the tree in matrix
       
    """
    Q = np.arange(len(distance)) # points
    V = np.array([]) # will contain vertices a,...
    E = [] # will contain edges (a,b)
    V = np.append(V,0)
    while len(V)!= len(Q): # Not all vertices used
        s = np.max(distance) # maximal value
        for k in range(len(V)): # look for every used vertex
            for i in range(len(Q)):
                if Q[i] not in V: # if new vertex is not used
                    if distance[int(V[k]),i] <= s: # find smallest distance
                        s = distance[int(V[k]),i]
                        j = i # memorize vertex position of new point
                        h = V[k] # memorize vertex from which new point is branching of
        V = np.append(V,j).astype(int)
        E = np.append(E,(h,j))
    E = np.reshape(E,(len(distance)-1,2)).astype(int)
    return E

def matching(tree,distances):
    """
    Search for vertices with odd number of edges. Matches these vertices with new edges with minimal distances.
    Input: tree_ minimal tree
           distances_ matrix conatining the distances
    Output: E_ minimal tree + matching edges -> result can create hamilton circle
    """
    M = np.array([])
    E = tree.flatten() #transform Matrix to 1d-array
    Count = np.zeros(len(distances)) 
    for z in range(len(distances)):# Count number of edges connected to a point
        for j in range(len(E)):
            if z == E[j]:
                Count[z]+=1
    Count = Count%2 # Check if number is even or odd
    for q in range(len(Count)):
        if Count[q]==1:
            M = np.append(M,q)# Odd vertices have to be matched
    while len(M)>0:# Match each vertex in M to another vertex in M via cheapest edge
        s = np.max(distances)
        for k in range(len(M)):
            for i in range(len(M)):
                if i != k:
                    if distances[int(M[k]),int(M[i])] <= s:
                        s = distances[int(M[k]),int(M[i])]
                        j = int(M[i])
                        h = int(M[k])
        # Add new edge to T and remove from the ones to be matched                
        E = np.append(E,(j,h))
        M = np.delete(M,np.where((M == j)))
        M = np.delete(M,np.where((M == h)))

    E = np.reshape(E,(len(E)//2,2)).astype(int)
    return E

def euler_circle(tree,start =0):
    """
    euler_cirlce creates an eulerpath given an euler-tree
    Input: tree - tree of edges [a,b], which contains an euler path
            start - start point - default is 0
    Output: euler-tree
    
    """
    E = np.copy(tree)
    Trail =np.array([]) # will get euler-circle
    for q in range(len(E)):
        if tree[q,0] ==start: # search starting edge
            break
    Trail = np.append(Trail,E[q])
    E = np.delete(E,q,0) # remove this edge from avalable edges
    while len(E)>0:
        test =0
        if Trail[0]!= Trail[-1]: # We do not have a circle
            test =1
            k = len(tree)+1 # Have we found the next edge?
            for q in range(len(E)): # We have abbc -> Look for edge [c,d]
                #print(E[q,0],Trail)
                if E[q,0] == Trail[-1]:
                    k = q
                    break  
            if k < len(tree):

                Trail = np.append(Trail,E[k]).astype(int)
                E = np.delete(E,k,0)
            if k > len(tree):

                for q in range(len(E)):# We have abbc -> Look for edge [d,c] and invert it
                    if E[q,1] == Trail[-1]:
                        k = q
                        break  
                if k < len(tree):
                    Trail = np.append(Trail,np.flip(E[k])).astype(int)
                    E = np.delete(E,k,0)
        else: # We do have a circle
            if test <1:

                for q in range(len(E)): 
                    if E[q,0] in Trail: # We have edge [d,f] search for vertex d in trail
                        if E[q,0]==Trail[-1]:
                            Trail = np.append(Trail,E[q]).astype(int)
                        else:
                            circle = np.where(Trail == E[q,0])
                            d = circle[0][0]

                            Trailleft = Trail[:d+1]
                            Trailright = Trail[d+1:]
                            Taril =np.append(Trailright,Trailleft)
                            Trail = np.append(Taril,E[q]).astype(int)

                        E = np.delete(E,q,0)
                        break
                    if E[q,1] in Trail:
                        if E[q,1]==Trail[-1]:
                            Trail = np.append(Trail,np.flip(E[q])).astype(int)
                        else:
                            circle = np.where(Trail == E[q,1])

                            d = circle[0][0]
                            Trailleft = Trail[:d+1]
                            Trailright = Trail[d+1:]
                            Taril =np.append(Trailright,Trailleft)
                            Trail = np.append(Taril,np.flip(E[q])).astype(int)

                        E = np.delete(E,q,0)
                        break
    Trail = np.reshape(Trail,(len(Trail)//2,2)).astype(int)         
    return Trail
        

def hamilton(euler_tree):
    """
    Input: Eulerian circuit_ Matrix of edges
    Output: Hamiltonian circuit_ 1d-array
    
    """
    euler = euler_tree.flatten()
    hamilton = np.array([])
    for x in range(len(euler)):
        if euler[x] not in hamilton: # Only add new numbers to hamilton circle
            hamilton = np.append(hamilton,euler[x]).astype(int)
    hamilton = np.append(hamilton,hamilton[0]) # add first vertex to get a closed circuit
    return hamilton

def christofides(distances,start=0):
    """
    Input: distances_ Matrix conatining distances between points
           start_Startpoint of sequence_default=0
    Output: solution of tsp with Christofides algorithm
    """
    min_tree = prim(distances)
    match = matching(min_tree,distances)
    euler = euler_circle(match,start)
    return hamilton(euler)

def christofides_all(A):
    """
    Input: distances_ Matrix conatining distances between points
    Output: Best solution of tsp with Christofides algorithm over all starting points
    """    
    dist= len(A)*np.max(A)
    for s in range(len(A)):
        if base.totalTravelDist(christofides(A,s),A)<dist:
            dist = base.totalTravelDist(tsp.christofides(A,s),A)
            path = christofides(A,s)
    return path

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
    points = np.append(points,points[0]) #Schließe die Punkte zu einem Kreis   #Neu
    pathWeights = np.zeros(tries+1)
    temps = np.zeros(tries+1)
    pathWeights[0] = base.totalTravelDist(points, dist_matrix)
    temps[0] = starting_temp
    cost = pathWeights[0]
    
    for i in range(tries):
        points = np.delete(points,-1)#Entferne Kreispunkt               #NEU
        new_sequence = base.Opt_method(method,points)
        new_sequence = np.append(new_sequence,new_sequence[0])#Schließe die Punkte zu einem Kreis #NEU 
        new_cost = base.totalTravelDist(new_sequence, dist_matrix)
        if np.random.uniform(low=0, high=1) < np.exp((pathWeights[i]-new_cost)/temps[i]):
            points = new_sequence
            cost = new_cost
        else:                                                           #NEU
            points = np.append(points,points[0])#Schließe die Punkte zu einem Kreis     #NEU
        pathWeights[i+1] = cost
        temps[i+1] = alpha*temps[i] 
    return(points, pathWeights, temps)
