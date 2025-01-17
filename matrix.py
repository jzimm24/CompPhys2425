import numpy as np

def create_testmatrix_2d(high, N, symmetric = True, low = 1, save ='0'): 
    """
    input: high: highest distance between two points - int or float
            N : number of points of interest -> dimension of matrix _int
            symmetric: default True, result will be symmetric matrix
            low: default 1, lowest possible distance _ int or float  
    output: random matrix for testpurpose
    """
    
    testmatrix = np.random.randint(low, high =high,size=(N,N))
    for i in range(N):
        testmatrix[i,i] = 0
    if symmetric:
        testmatrix = (testmatrix+testmatrix.T)/2
        np.savetxt('testmatrix_sym_('+str(low)+'_'+str(high)+')_N'+str(N)+'_'+str(save)+'.txt', testmatrix)
    else:
        np.savetxt('testmatrix_('+str(low)+'_'+str(high)+')_N'+str(N)+'_'+str(save)+'.txt', testmatrix)
    return testmatrix

def create_testmatrix_3d(high, N, time, symmetric = True, low = 1, save ='0'): 
    """
    input: high: highest distance between two points - int or float
            N : number of points of interest -> dimension of matrix _int
            time : number of different time matrices
            symmetric: default True, result will be symmetric matrix
            low: default 1, lowest possible distance _ int or float  
    output: random matrix for testpurpose
    """
    
    testmatrix = np.random.randint(low, high =high,size=(N,N,time))
    for j in range(time):
        for i in range(N):
            testmatrix[i,i,j] = 0
    if symmetric:
        for i in range(time):
            testmatrix[:,:,i] = (testmatrix[:,:,i]+testmatrix[:,:,i].T)/2
        with open('testmatrix_sym_('+str(low)+'_'+str(high)+')_N'+str(N)+'_t'+str(time)+'_'+str(save)+'.txt', 'w') as outfile:

            outfile.write('# Array shape: {0}\n'.format(testmatrix.shape))

            for data_slice in testmatrix:

                np.savetxt(outfile, data_slice, fmt='%-7.2f')

                # Writing out a break to indicate different slices...
                outfile.write('# New slice\n')
    else:
        with open('testmatrix_('+str(low)+'_'+str(high)+')_N'+str(N)+'_t'+str(time)+'_'+str(save)+'.txt', 'w') as outfile:

            outfile.write('# Array shape: {0}\n'.format(testmatrix.shape))

            for data_slice in testmatrix:

                np.savetxt(outfile, data_slice, fmt='%-7.2f')

                # Writing out a break to indicate different slices...
                outfile.write('# New slice\n')
    return testmatrix
        
def load_matrix(name): 
    """
        loads previously randomly generated saved matrix    
        input: savename of testmatrix: 'testmatrix__('+str(low)+'_'+str(high)+')_'+str(save)+'.txt'
        output: testmatrix
    """
    data = np.loadtxt(name)
    return data