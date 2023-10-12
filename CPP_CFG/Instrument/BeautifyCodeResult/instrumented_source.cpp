#include<iostream> 

//in the name of allah
#include <fstream>
std::ofstream logFile("log_file.txt");

using namespace std;
int main()
  {
logFile << "1 1" << std::endl;

    int x = 5;
    if(logFile << "1 1" << std::endl && (x < 7))
      {
logFile << "1 2" << std::endl;

        x += 2;
      }
    else
      {
logFile << "1 3" << std::endl;

        x += 5;
      }
logFile << "1 4" << std::endl;

    x = 9;
  }
