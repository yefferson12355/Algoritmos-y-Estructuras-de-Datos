#include<iostream>
using namespace std;

int main()
{
    int precios[]={1,2,3,4,5};
    for (int i = 0; i < 5; i++)
    {
        cout<<precios[i];
    }
    for ( int x:precios)
    {
        cout<<x;
    }
    
    
    return 0;
}
