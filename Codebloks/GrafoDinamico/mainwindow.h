#ifndef MAINWINDOW_H
#define MAINWINDOW_H
#include <QMainWindow>
#include <vector>
#include <string>
#include <unordered_map>
#include "grafowidget.h" // Incluimos la cabecera de nuestro widget

// Declaraciones adelantadas para no incluir todo Qt en el .h
class QTextEdit;
class QLineEdit;
class QPushButton;

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void cargarGrafoDesdeTexto();
    void buscarRuta();

private:
    void setupUi();
    // Implementación de Dijkstra
    void dijkstra(const std::string& inicio);

    // Componentes de la UI
    QTextEdit* entradaTextArea;
    QLineEdit* inicioField;
    QLineEdit* finField;
    QPushButton* crearGrafoButton;
    QPushButton* buscarRutaButton;
    QTextEdit* resultadoArea;
    GrafoWidget* grafoWidget; // Nuestro lienzo

    // Datos del grafo
    std::unordered_map<std::string, Nodo> m_nodos;
    std::vector<Arista> m_aristas;
    std::vector<std::string> m_rutaCorta;

    // Resultados de Dijkstra
    std::unordered_map<std::string, int> m_distancias;
    std::unordered_map<std::string, std::string> m_padres;
};
#endif // MAINWINDOW_H