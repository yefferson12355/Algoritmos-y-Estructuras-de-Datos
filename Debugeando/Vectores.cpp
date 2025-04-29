#include <iostream>  // Para imprimir en consola
#include <vector>    // ÚNICA LIBRERÍA: std::vector

int main() {
    // Crear un vector de enteros con valores iniciales
    std::vector<int> vec = {10, 20, 30};

    // Mostrar elementos usando for tradicional
    std::cout << "Elementos del vector: ";
    for (size_t i = 0; i < vec.size(); ++i)  // size() devuelve el número de elementos
        std::cout << vec[i] << " ";  // Acceso por índice
    std::cout << "\n";

    // Agregar elementos al final
    vec.push_back(40);  // push_back(): añade al final
    vec.push_back(50);

    // Acceder al primer y último elemento
    std::cout << "Primer elemento: " << vec.front() << "\n";  // front(): primer valor
    std::cout << "Último elemento: " << vec.back() << "\n";   // back(): último valor

    // Acceder con .at(), con verificación de límites
    std::cout << "Elemento en posición 2: " << vec.at(2) << "\n";  // at(): acceso seguro

    // Insertar en una posición específica
    vec.insert(vec.begin() + 1, 15);  // insert(): insertar en una posición

    // Eliminar un elemento en una posición específica
    vec.erase(vec.begin() + 3);  // erase(): elimina el elemento en la posición

    // Mostrar elementos usando range-based for loop
    std::cout << "Vector actualizado: ";
    for (int val : vec)
        std::cout << val << " ";
    std::cout << "\n";

    // Eliminar el último elemento
    vec.pop_back();  // pop_back(): elimina el último valor

    // Tamaño del vector
    std::cout << "Tamaño actual: " << vec.size() << "\n";  // size(): cantidad de elementos

    // Capacidad reservada del vector
    std::cout << "Capacidad reservada: " << vec.capacity() << "\n";  // capacity(): espacio reservado

    // Redimensionar el vector
    vec.resize(6);  // resize(): cambiar el tamaño (rellena con ceros si se agranda)
    std::cout << "Tamaño tras resize(6): " << vec.size() << "\n";

    // Verificar si el vector está vacío
    std::cout << "¿Está vacío? " << (vec.empty() ? "Sí" : "No") << "\n";  // empty(): verifica si está vacío

    // Limpiar el vector
    vec.clear();  // clear(): elimina todos los elementos

    // Verificar estado final
    std::cout << "Tamaño tras clear(): " << vec.size() << "\n";
    std::cout << "¿Está vacío? " << (vec.empty() ? "Sí" : "No") << "\n";

    return 0;
}
