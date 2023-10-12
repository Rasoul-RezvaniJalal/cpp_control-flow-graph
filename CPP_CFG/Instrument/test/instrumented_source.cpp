
//in the name of allah
#include <fstream>
std::ofstream logFile("log_file.txt");

int main()
  {
logFile << "1 1" << std::endl;

    int x = 0;
    if(logFile << "1 1" << std::endl && (x==4))
      {
logFile << "1 2" << std::endl;

        cout<<"here";
      }
    else
      {
logFile << "1 3" << std::endl;

        cout<<"bye";
      }
logFile << "1 4" << std::endl;

    cout<<"end";
  }