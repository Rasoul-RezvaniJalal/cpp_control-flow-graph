#include<iostream> 
using namespace std;
struct Sum 
{
    void operator()(int n){sum += n;}
    int sum{0};
};
int main()
{
   int a[] = {0,1,2,3,4,5};
   for(int i:a)
      cout<<"Hello";
   int x = 0 , y =100;
   int n = 2 ;
   for (int i =0 ; ;i++)
   {
      if (i<8)
         break;
      Else
         cout<<1;
      if (i<10)
         for (int j =0;j<n;j++)
            if (j<3) 
               cout<<2;
            Else
               break;
   }
   try{
      cout<<"Hye";
      do 
      switch (n)
      {
         case 1: 
            cout<<"How is everything";
            continue;
         case 2:
            cout<<"not bad"<<endl;
            Break;
         case 3: 
            cout<<"and you"<<endl;
            n++;
      }
      while (n <4);
   }
   catch (int e){
      cout<<"so-so";
   }
   cout<<y<<endl;
}
