#include<iostream> 

//in the name of allah
#include <fstream>
std::ofstream logFile("log_file.txt");

using namespace std;
int OUT_OF_RANGE = -2;
int INVALID = -1;
int SCALENE = 0;
int ISOSELES = 1;
int EQUILATERAL = 2;
int triangle(int a, int b, int c) 
{
logFile << "1 1" << std::endl;

 boolean c1, c2, c3, isATriangle;
 // Step 1: Validate Input
 c1 = (1 <= a) && (a <= 200);
 c2 = (1 <= b) && (b <= 200);
 c3 = (1 <= c) && (c <= 200);
 int triangleType = INVALID;
 if (logFile << "1 1" << std::endl && (!c1 || !c2 || !c3))
 {
logFile << "1 2" << std::endl;
triangleType = OUT_OF_RANGE;
}
 else 
 {
logFile << "1 3" << std::endl;

 // Step 2: Is A Triangle?
 if (logFile << "1 3" << std::endl && ((a < b + c) && (b < a + c) && (c < a + b)))
 {
logFile << "1 4" << std::endl;
isATriangle = true;
}
 else
 {
logFile << "1 5" << std::endl;
isATriangle = false;
}
logFile << "1 6" << std::endl;

 // Step 3: Determine Triangle Type
 if (logFile << "1 6" << std::endl && (isATriangle)) 
 {
logFile << "1 7" << std::endl;

 if (logFile << "1 7" << std::endl && ((a == b) && (b == c)))
 {
logFile << "1 8" << std::endl;
triangleType = EQUILATERAL;
}
 else {
logFile << "1 9" << std::endl;
if (logFile << "1 9" << std::endl && ((a != b) && (a != c) && (b != c)))
 {
logFile << "1 10" << std::endl;
triangleType = SCALENE;
}
 else
 {
logFile << "1 11" << std::endl;
triangleType = ISOSELES;
}
logFile << "1 12" << std::endl;

logFile << "1 12" << std::endl;

 } 
 else
 {
logFile << "1 13" << std::endl;
triangleType = INVALID;
}
logFile << "1 14" << std::endl;

 }
logFile << "1 15" << std::endl;

 return triangleType;
}
