// -------------------- CLASE PERSONA --------------------
    class Persona
    {
        public string Nombre { get; set; }
        public int Edad { get; set; }
        public bool EsEstudiante { get; set; }
        public List<string> Asignaturas { get; set; }

        public Persona(string nombre, int edad, bool esEstudiante, List<string> asignaturas)
        {
            Nombre = nombre;
            Edad = edad;
            EsEstudiante = esEstudiante;
            Asignaturas = asignaturas;
        }

        public void MostrarInformacion()
        {
            Console.WriteLine($"\nInformación de la persona:");
            Console.WriteLine($"Nombre: {Nombre}");
            Console.WriteLine($"Edad: {Edad}");
            Console.WriteLine($"Estudiante: {EsEstudiante}");
            Console.WriteLine("Asignaturas: " + string.Join(", ", Asignaturas));
        }
    }


    class Lenguaje 
    {
        private string nombre;
        private int año;
        
        public Lenguaje(string nombre, int año)
        {
            this.nombre = nombre;
            this.año = año;
        }
        public void DescribirLenguaje()
        {
            Console.WriteLine("{0} fue creado en {1}", this.nombre, this.año);
        }
    }
    