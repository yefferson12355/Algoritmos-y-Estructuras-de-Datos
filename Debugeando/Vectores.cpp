#include <iostream>
#include <vector>
using namespace std;

//
int main()
{
    vector<int> precios = {1, 2, 3, 4, 5};
    // Recorre el vector usando un bucle for tradicional
    for (int i = 0; i < precios.size(); i++)
    {
        cout << precios[i];
    }
    //Recorre el vector usando un bucle for-each (rango basado en el valor)
    for(int i : precios)
    {
        cout << i ;
    }
    return 0;
}
