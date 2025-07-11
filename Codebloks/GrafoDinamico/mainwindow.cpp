#include "mainwindow.h"
#include <QTextEdit>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QMessageBox>
#include <QSplitter>

#include <sstream>
#include <queue>
#include <limits>
#include <algorithm>
#include <random>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    setupUi();
}

MainWindow::~MainWindow() {}

void MainWindow::setupUi() {
    // Panel de entrada
    entradaTextArea = new QTextEdit;
    entradaTextArea->setText("A B 4\nA C 2\nB D 10\nC D 3\nC E 8\nD E 6");
    crearGrafoButton = new QPushButton("Crear Grafo");
    QHBoxLayout* topLayout = new QHBoxLayout;
    topLayout->addWidget(new QLabel("Ingrese aristas (Nodo1 Nodo2 Peso):"));
    topLayout->addWidget(entradaTextArea);
    topLayout->addWidget(crearGrafoButton);
    QWidget* topWidget = new QWidget;
    topWidget->setLayout(topLayout);

    // Panel de búsqueda
    inicioField = new QLineEdit;
    finField = new QLineEdit;
    buscarRutaButton = new QPushButton("Buscar Ruta");
    resultadoArea = new QTextEdit;
    resultadoArea->setReadOnly(true);
    QHBoxLayout* bottomLayout = new QHBoxLayout;
    bottomLayout->addWidget(new QLabel("Inicio:"));
    bottomLayout->addWidget(inicioField);
    bottomLayout->addWidget(new QLabel("Fin:"));
    bottomLayout->addWidget(finField);
    bottomLayout->addWidget(buscarRutaButton);
    bottomLayout->addWidget(resultadoArea);
    QWidget* bottomWidget = new QWidget;
    bottomWidget->setLayout(bottomLayout);

    // Lienzo para el grafo
    grafoWidget = new GrafoWidget;

    // Layout principal con un splitter
    QSplitter *splitter = new QSplitter(Qt::Vertical);
    splitter->addWidget(topWidget);
    splitter->addWidget(grafoWidget);
    splitter->addWidget(bottomWidget);
    splitter->setStretchFactor(1, 1); // Hace que el grafo ocupe más espacio

    setCentralWidget(splitter);
    setWindowTitle("Grafo Transporte C++/Qt");

    // Conectar señales a slots
    connect(crearGrafoButton, &QPushButton::clicked, this, &MainWindow::cargarGrafoDesdeTexto);
    connect(buscarRutaButton, &QPushButton::clicked, this, &MainWindow::buscarRuta);
    
    // Carga inicial
    cargarGrafoDesdeTexto();
}

void MainWindow::cargarGrafoDesdeTexto() {
    m_nodos.clear();
    m_aristas.clear();
    m_rutaCorta.clear();

    std::string texto = entradaTextArea->toPlainText().toStdString();
    std::stringstream ss(texto);
    std::string linea;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distribX(50, 750);
    std::uniform_int_distribution<> distribY(50, 550);

    while (std::getline(ss, linea)) {
        std::stringstream ls(linea);
        std::string n1_str, n2_str;
        int peso;
        if (ls >> n1_str >> n2_str >> peso) {
            if (m_nodos.find(n1_str) == m_nodos.end()) {
                m_nodos[n1_str] = {n1_str, {distribX(gen), distribY(gen)}};
            }
            if (m_nodos.find(n2_str) == m_nodos.end()) {
                m_nodos[n2_str] = {n2_str, {distribX(gen), distribY(gen)}};
            }
            // Añadimos arista en una dirección (el dibujo se encarga del resto)
            m_aristas.push_back({n1_str, n2_str, peso});
        }
    }
    grafoWidget->setDatos(&m_nodos, &m_aristas, &m_rutaCorta);
}

void MainWindow::buscarRuta() {
    std::string inicioTexto = inicioField->text().toStdString();
    std::string finTexto = finField->text().toStdString();

    if (m_nodos.find(inicioTexto) == m_nodos.end() || m_nodos.find(finTexto) == m_nodos.end()) {
        QMessageBox::warning(this, "Error", "Nodos inválidos");
        return;
    }

    dijkstra(inicioTexto);

    if (m_distancias.find(finTexto) == m_distancias.end() || m_distancias.at(finTexto) == std::numeric_limits<int>::max()) {
        resultadoArea->setText("No hay camino");
        m_rutaCorta.clear();
    } else {
        m_rutaCorta.clear();
        std::string actual = finTexto;
        while (m_padres.count(actual)) {
            m_rutaCorta.push_back(actual);
            actual = m_padres[actual];
        }
        m_rutaCorta.push_back(inicioTexto);
        std::reverse(m_rutaCorta.begin(), m_rutaCorta.end());

        std::string rutaStr = "Ruta más corta: ";
        for(const auto& n : m_rutaCorta) {
            rutaStr += n + " ";
        }
        rutaStr += "\nDistancia: " + std::to_string(m_distancias.at(finTexto));
        resultadoArea->setText(QString::fromStdString(rutaStr));
    }

    grafoWidget->setDatos(&m_nodos, &m_aristas, &m_rutaCorta);
}

void MainWindow::dijkstra(const std::string& inicio) {
    m_distancias.clear();
    m_padres.clear();
    
    // Cola de prioridad (min-heap)
    using Par = std::pair<int, std::string>;
    std::priority_queue<Par, std::vector<Par>, std::greater<Par>> pq;

    for (const auto& par : m_nodos) {
        m_distancias[par.first] = std::numeric_limits<int>::max();
    }

    m_distancias[inicio] = 0;
    pq.push({0, inicio});

    while (!pq.empty()) {
        int d = pq.top().first;
        std::string u = pq.top().second;
        pq.pop();

        if (d > m_distancias[u]) continue;

        for (const auto& arista : m_aristas) {
            // Grafo no dirigido, chequear ambas direcciones
            std::string v;
            if (arista.desde == u) v = arista.hasta;
            else if (arista.hasta == u) v = arista.desde;
            else continue;

            if (m_distancias[u] + arista.peso < m_distancias[v]) {
                m_distancias[v] = m_distancias[u] + arista.peso;
                m_padres[v] = u;
                pq.push({m_distancias[v], v});
            }
        }
    }
}