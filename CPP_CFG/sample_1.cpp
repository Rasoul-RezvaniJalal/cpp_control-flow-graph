
#include<stdio.h>
#include<stdlib.h>
using namespace std;

int main()
{
 int x = 3;
 do
 {
     x-=1;
     cout<<"12";
     if(x==0)
        cout<<"end";
     else
        continue;

    cout<<"sth";
 }while(x>0);
    return 0;
}
