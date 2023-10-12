#include<stdio.h>
#include<stdlib.h>

//in the name of allah
#include <fstream>
std::ofstream logFile("log_file.txt");

using namespace std;
int main()
  {
logFile << "1 1" << std::endl;

    int x = 3;
    do
    {
logFile << "1 2" << std::endl;

      x-=1;
      cout<<"12";
      if(logFile << "1 2" << std::endl && (x==0))
        {
logFile << "1 3" << std::endl;
cout<<"end";
}
      else
        {
logFile << "1 4" << std::endl;
continue;
}
logFile << "1 5" << std::endl;

      cout<<"sth";
    }while(logFile << "1 2" << std::endl && (x>0));
logFile << "1 6" << std::endl;

    return 0;
  }
