using System;
using System.Collections.Generic;

class Program
{
    static void Main(string[] args)
    {
        List<int> números = new List<int> { 23, 45, 16, 37, 3, 99, 22 };
        List<int> listaOrdenada = quicksort(números);

        Console.WriteLine("Lista ordenada:");
        foreach (int num in listaOrdenada)
        {
            Console.Write(num + " ");
        }
        Console.WriteLine();
    }

    static List<int> quicksort(List<int> lista)
    {
        if (lista.Count <= 1)
        {
            return new List<int>(lista);
        }

        int pivote = lista[0];
        List<int> menores = new List<int>();
        List<int> mayores = new List<int>();

        for (int i = 1; i < lista.Count; i++)
        {
            if (lista[i] < pivote)
            {
                menores.Add(lista[i]);
            }
            else
            {
                mayores.Add(lista[i]);
            }
        }

        List<int> resultado = new List<int>();
        resultado.AddRange(quicksort(menores));
        resultado.Add(pivote);
        resultado.AddRange(quicksort(mayores));

        return resultado;
    }
}
