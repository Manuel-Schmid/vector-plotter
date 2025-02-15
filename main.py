import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import pyqtgraph.opengl as gl

class VectorPlot3D(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Vector and Plane Plotter")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212; color: white;")

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # 3D View
        self.view = gl.GLViewWidget()
        self.view.setBackgroundColor(QColor(18, 18, 18))  # Dark mode
        layout.addWidget(self.view)

        # Add Grid
        grid = gl.GLGridItem()
        grid.setSize(10, 10, 1)
        grid.setSpacing(1, 1, 1)
        self.view.addItem(grid)

        # Add Buttons
        self.btn_add_vector = QPushButton("Add Random Vector")
        self.btn_add_vector.clicked.connect(self.add_vector)
        layout.addWidget(self.btn_add_vector)

        self.btn_add_plane = QPushButton("Add Plane")
        self.btn_add_plane.clicked.connect(self.add_plane)
        layout.addWidget(self.btn_add_plane)

        self.vectors = []
        self.planes = []

    def add_vector(self):
        vec = np.random.rand(3) * 4 - 2  # Random vector from -2 to 2
        color = (1, 0, 0, 1)  # Red

        arrow = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], vec]),
            color=color,
            width=3,
            mode='lines'
        )
        self.view.addItem(arrow)
        self.vectors.append(arrow)

    def add_plane(self):
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        x, y = np.meshgrid(x, y)
        z = np.zeros_like(x)  # Plane at z=0

        pts = np.vstack((x.ravel(), y.ravel(), z.ravel())).T
        mesh = gl.GLScatterPlotItem(pos=pts, color=(0, 0, 1, 0.3), size=2)
        self.view.addItem(mesh)
        self.planes.append(mesh)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VectorPlot3D()
    window.show()
    sys.exit(app.exec())
