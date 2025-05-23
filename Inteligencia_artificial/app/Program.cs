using System;
using System.Collections.Generic;

namespace ReconocimientoDeSeñas
{
    class Program
    {
        // Función para sumar dos números (fuera de Main)
        static int Sumar(int num1, int num2)
        {
            return num1 + num2;
        }

        static void Main(string[] args)
        {
            Console.WriteLine("¡Hola mundo!");

            // -------------------- VARIABLES --------------------
            string nombre = "Juan";
            int edad = 25;
            bool esEstudiante = true;
            Console.WriteLine($"Nombre: {nombre}, Edad: {edad}, ¿Es estudiante?: {esEstudiante}");

            // -------------------- ARRAYS --------------------
            int[] calificaciones = new int[3];
            calificaciones[0] = 90;
            calificaciones[1] = 85;
            calificaciones[2] = 95;
            Console.WriteLine("Primera calificación: " + calificaciones[0]);

            // -------------------- ARRAY DINÁMICO --------------------
            dynamic[] datosMixtos = { "Juan", 25, true };
            Console.WriteLine("Nombre desde array dinámico: " + datosMixtos[0]);

            // -------------------- LISTAS --------------------
            List<string> asignaturas = new List<string> { "Matemáticas", "Programación", "Física" };
            asignaturas.Add("Química");
            asignaturas.Remove("Física");
            Console.WriteLine("Asignaturas: " + string.Join(", ", asignaturas));

            // -------------------- DICCIONARIOS --------------------
            Dictionary<int, string> jugadores = new Dictionary<int, string>();
            jugadores.Add(1, "Juan");
            jugadores.Add(2, "Pedro");
            Console.WriteLine("Jugador con ID 1: " + jugadores[1]);

            // -------------------- CONSTANTES --------------------
            const string NombreConst = "Juan";
            const int EdadConst = 25;
            const bool EsEstudianteConst = true;
            const double pi = 3.14159265358979323846;
            Console.WriteLine($"Constantes utilizadas: Nombre={NombreConst}, Edad={EdadConst}, Estudiante={EsEstudianteConst}, Pi={pi}");

            // -------------------- OPERADORES --------------------
            int a = 5;
            int b = 10;
            int c = a + b;
            Console.WriteLine("Resultado de la suma: " + c);
            Console.WriteLine(1 + 1);
            Console.WriteLine(1 - 1);
            Console.WriteLine(1 * 1);
            Console.WriteLine(1 / 1);
            Console.WriteLine(1 % 1);
            Console.WriteLine(1 == 1);
            Console.WriteLine(1 != 1);
            Console.WriteLine(1 > 1);
            Console.WriteLine(1 < 1);
            Console.WriteLine(true || true);
            Console.WriteLine(true || false);
            Console.WriteLine(false || true);
            Console.WriteLine(false || false);
            Console.WriteLine(true && true);
            Console.WriteLine(true && false);
            Console.WriteLine(!true);
            Console.WriteLine(1 << 1);

            // -------------------- CONDICIONALES --------------------
            bool autorizado = true;
            if (autorizado)
            {
                Console.WriteLine("Acceso permitido");
            }
            else
            {
                Console.WriteLine("Acceso denegado");
            }

            if (1 == 1)
            {
                Console.WriteLine("1 es igual a 1");
            }
            else if (1 > 1)
            {
                Console.WriteLine("1 es mayor que 1");
            }
            else if (1 < 1)
            {
                Console.WriteLine("1 es menor que 1");
            }
            else
            {
                Console.WriteLine("1 es diferente de 1");
            }

            int edadmi = 18;
            switch (edadmi)
            {
                case 18:
                    Console.WriteLine("Eres mayor de edad");
                    break;
                case 17:
                    Console.WriteLine("Eres menor de edad");
                    break;
                default:
                    Console.WriteLine("No se puede determinar la edad");
                    break;
            }

            // -------------------- FUNCIONES --------------------
            int sumar(int num1, int num2) // función local para sumar
            {
                return num1 + num2;
            }
            int suma = sumar(5, 10);
            Console.WriteLine("Suma: " + suma);

            void mostrarMensaje(string mensaje) // función local para mostrar mensajes
            {
                Console.WriteLine(mensaje);
            }
            mostrarMensaje("Este es un mensaje desde la función local");

            void multiplicar(int num1, int num2) // función local sin retorno
            {
                Console.WriteLine("Multiplicación: " + (num1 * num2));
            }
            multiplicar(5, 10);

            // -------------------- BUCLES --------------------
            for (int i = 0; i < 5; i++)
            {
                Console.WriteLine("Bucle for: " + i);
            }

            string[] nombres = { "Juan", "Pedro", "María" };
            foreach (string nom in nombres) // ← cambiamos 'nombre' por 'nom' para evitar el error CS0136
            {
                Console.WriteLine("Bucle foreach: " + nom);
            }


            //--------------------------------- WHILE --------------------
            int entero = 100;
            int emergencia = 120;

            while (entero <= emergencia)
            {
                Console.WriteLine( entero);
                entero++;
            }

            Lenguaje lenguaje = new Lenguaje("C#", 2000);
            lenguaje.DescribirLenguaje();

            // -------------------- OBJETOS --------------------

            Persona persona = new Persona(nombre, edad, esEstudiante, asignaturas);
            persona.MostrarInformacion();

        }
    }
}
