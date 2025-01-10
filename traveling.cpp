#include <iostream>
#include <fstream>
#include <vector>
#include <random>
//TODO: -make functioning library (new file with class initialization and class funtions)
//      -make structure of code -> built classes
//      -test code
//      -make integtration to python for data analysis... 
//      -code Marcov chains and actually practical tp code not just rigorus comparison code !!!!!!!!!!!!!!!!!!!!!!!!!



//make random matrix of size n
std::vector<std::vector<double>> randomMatrix(int n){
    //initialize random number generator
    srand(time(NULL));
    
    //create nxn matrix with random number in each entry

    std::vector<std::vector<double>> matrix(n, std::vector<double>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            matrix[i][j] = (rand() % 100) + 1; // Generate a random real number between 1 and 100 as matrix entry
        }
    }
    return matrix;
}

//make random symmetric matrix of size n
std::vector<std::vector<double>> randomSymMatrix(int n){
    
    std::vector<std::vector<double>> symMatrix; //symmetric matrix storage
    std::vector<std::vector<double>> matrix = randomMatrix(n); //make random unsymmetric matrix of size nxn
    for (int i = 0; i < n; ++i) {   //make a symmetric matrix
        for (int j = 0; j < n; ++j) {
            symMatrix[i][j] = (matrix[i][j] + matrix[j][i])/2;
            symMatrix[j][i] = symMatrix[i][j];
        }
    }
    return symMatrix;
}

//writing matrix into file
int saveMatrix(std::string path, std::vector<std::vector<double>> matrix){
    std::ofstream myfile;   //initialize of object
    myfile.open("path");       // open file to write in
    int len = (matrix[0]).size();
    for (int i = 0; i < len; i++){
        for (int j = 0; j < len; j++){
            myfile<<matrix[i][j]<<" ";  //write the single matrix elements in to the file
        }
        myfile<<std::endl;
    }
    myfile.close(); //close the file

    return 1;
}

//getting matrix from file
std::vector<std::vector<double>> getMatrix(std::string path, std::vector<std::vector<double>> matrix){

    std::ifstream file("path"); //initializing fstream object
    for (int i = 0; i<matrix.size(); i++){    //making loops over both the rows and the columns
        for (int j = 0; j<matrix[0].size(); j++){
            file >>matrix[i][j];    //writting the data out of the file and into the matrix (2d vecotr object)
        }
    }
    file.close(); //close file

    return matrix;
}

//create random starting path
/*
std::vector<int> path(int n){
    std::vector<int> points; //determine number of points that have to be visited
    for (int i = 0; i<n; i++){
        points[i] = i;
    }
    
    srand(time(NULL));
    std::vector<int> randomPath = std::shuffle(&points[0], &points[n-1]);  //make random path visiting all points

    return randomPath;
}
*/

//pushback sequence (array) to std::vector
void pushbackSeq(int a[], int n, std::vector<int> vec)
{
    for (int i = 0; i < n; i++)
        vec.push_back(a[i]);
}

//create all possible paths (Heap's algorithm)
void heapPermutation(int a[], int size, int n, std::vector<int> permutations){
    // if size becomes 1 then write the obtained permutation into the array of paths "permutations"
    
    if (size == 1) {
        pushbackSeq(a, n, permutations);
        return;
    }
 
    for (int i = 0; i < size; i++) {
        heapPermutation(a, size - 1, n, permutations);
 
        // if size is odd, swap 0th i.e (first) and (size-1)th i.e (last) element
        if (size % 2 == 1)
            std::swap(a[0], a[size - 1]);
 
        // If size is even, swap ith and (size-1)th i.e (last) element
        else
            std::swap(a[i], a[size - 1]);
    }
}


//determine path weight
int pathWeight(std::vector<int> p, std::vector<std::vector<double>> distances, bool loop = 1){
    double sum = 0;
    for (int i = 0; i < p.size() - 1; i++){
        int start = p[i];
        int end = p[i+1];
        sum += distances[start][end];
    }
    if (loop){
        sum += distances[p.back()][p[0]];
    }
    
    return sum;
}

//find best path by comparison of all paths (only save best path and lowest cost)
struct path {   // struct that combines a path and its weight
  std::vector<int> sequence;
  int weight;
};

path bestPath_absolute(std::vector<int> points, std::vector<std::vector<double>> matrix){
    std::vector<int> possiblePaths;
    path currentBest;

    currentBest.sequence = points;
    currentBest.weight = pathWeight(points, matrix, 1);

    int* arr = &points[0];

    heapPermutation(arr, points.size(), points.size(), possiblePaths);
    for (int i = 1; i<(possiblePaths.size()/points.size()); i++){
        std::vector<int> subvec = {possiblePaths[points.size()*i], possiblePaths[points.size()*i + points.size()]};
        int currentWeight = pathWeight(subvec, matrix, 1);
        if (currentWeight < currentBest.weight){
            currentBest.weight = currentWeight;
            currentBest.sequence = subvec;
        }
    }

    return currentBest;
}



int main(){
    std::cout<<"Hello World!"<<std::endl;
    return 1;
}