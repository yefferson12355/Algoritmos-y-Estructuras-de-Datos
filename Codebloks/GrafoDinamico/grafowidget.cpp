#include "grafowidget.h"
#include <QPainter>
#include <QPaintEvent>

GrafoWidget::GrafoWidget(QWidget *parent) : QWidget(parent) {
    // Fondo blanco y tamaño mínimo
    setAutoFillBackground(true);
    QPalette pal = palette();
    pal.setColor(QPalette::Window, Qt::white);
    setPalette(pal);
    setMinimumSize(400, 300);
}

void GrafoWidget::setDatos(const std::unordered_map<std::string, Nodo>* nodos,
                         const std::vector<Arista>* aristas,
                         const std::vector<std::string>* rutaCorta) {
    m_nodos = nodos;
    m_aristas = aristas;
    m_rutaCorta = rutaCorta;
    update(); // Solicita un redibujado
}

void GrafoWidget::paintEvent(QPaintEvent *event) {
    QWidget::paintEvent(event);

    if (!m_nodos || !m_aristas) return;

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    // 1. Dibujar todas las aristas
    for (const auto& arista : *m_aristas) {
        if (m_nodos->count(arista.desde) && m_nodos->count(arista.hasta)) {
            QPoint p1 = m_nodos->at(arista.desde).pos;
            QPoint p2 = m_nodos->at(arista.hasta).pos;

            painter.setPen(QPen(Qt::gray, 1));
            painter.drawLine(p1, p2);

            painter.setPen(Qt::black);
            painter.drawText((p1 + p2) / 2, QString::number(arista.peso));
        }
    }

    // 2. Dibujar la ruta corta (si existe)
    if (m_rutaCorta && m_rutaCorta->size() > 1) {
        painter.setPen(QPen(Qt::red, 3));
        for (size_t i = 0; i < m_rutaCorta->size() - 1; ++i) {
            QPoint p1 = m_nodos->at((*m_rutaCorta)[i]).pos;
            QPoint p2 = m_nodos->at((*m_rutaCorta)[i + 1]).pos;
            painter.drawLine(p1, p2);
        }
    }

    // 3. Dibujar todos los nodos
    for (const auto& par : *m_nodos) {
        const Nodo& nodo = par.second;
        painter.setBrush(QColor(102, 204, 255));
        painter.setPen(QPen(Qt::black, 1));
        painter.drawEllipse(nodo.pos, 15, 15);
        painter.drawText(QRect(nodo.pos - QPoint(15, 15), QSize(30, 30)), Qt::AlignCenter, QString::fromStdString(nodo.nombre));
    }
}