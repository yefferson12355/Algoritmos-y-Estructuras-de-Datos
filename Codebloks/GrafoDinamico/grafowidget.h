#ifndef GRAFOWIDGET_H
#define GRAFOWIDGET_H

#include <QWidget>
#include <string>
#include <vector>
#include <unordered_map>
#include <QPoint>

// Estructuras para representar el grafo
struct Nodo {
    std::string nombre;
    QPoint pos; // Usamos QPoint de Qt para las coordenadas
};

struct Arista {
    std::string desde;
    std::string hasta;
    int peso;
};

class GrafoWidget : public QWidget {
    Q_OBJECT

public:
    explicit GrafoWidget(QWidget *parent = nullptr);

    // Funciones para pasar los datos del grafo desde la ventana principal
    void setDatos(const std::unordered_map<std::string, Nodo>* nodos,
                  const std::vector<Arista>* aristas,
                  const std::vector<std::string>* rutaCorta);

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    const std::unordered_map<std::string, Nodo>* m_nodos = nullptr;
    const std::vector<Arista>* m_aristas = nullptr;
    const std::vector<std::string>* m_rutaCorta = nullptr;
};

#endif // GRAFOWIDGET_H