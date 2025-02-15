import math
import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMenuBar, QDockWidget, QLabel, \
    QLineEdit, QPushButton, QFormLayout, QCheckBox
from PyQt6.QtGui import QColor, QAction
from PyQt6.QtCore import Qt
import pyqtgraph.opengl as gl


class VectorPlot3D(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Vector and Plane Plotter")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212; color: white;")

        # Settings Dock (Visible by default, collapsible)
        self.dock = QDockWidget("Settings", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        settings_widget = QWidget()
        settings_layout = QFormLayout()

        self.vector_input = QLineEdit()
        self.vector_input.returnPressed.connect(self.add_custom_vector)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")

        self.add_custom_vector_btn = QPushButton("Plot Custom Vector")
        self.add_custom_vector_btn.clicked.connect(self.add_custom_vector)
        self.add_random_vector_btn = QPushButton("Add Random Vector")
        self.add_random_vector_btn.clicked.connect(self.add_random_vector)
        self.add_random_plane_btn = QPushButton("Add Random Plane")
        self.add_random_plane_btn.clicked.connect(self.add_random_plane)

        settings_layout.addRow(QLabel("Enter Vector (x, y, z):"), self.vector_input)
        settings_layout.addRow(self.error_label)
        settings_layout.addRow(self.add_custom_vector_btn)
        settings_layout.addRow(self.add_random_vector_btn)
        # settings_layout.addRow(self.add_random_plane_btn)

        # Toggle Format Button
        self.toggle_format_btn = QCheckBox("Parameter Form")
        self.toggle_format_btn.stateChanged.connect(self.update_display)
        settings_layout.addRow(self.toggle_format_btn)

        # Display Vectors and Planes
        self.display_label = QLabel()
        settings_layout.addRow(self.display_label)

        settings_widget.setLayout(settings_layout)
        self.dock.setWidget(settings_widget)

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
        grid.setSize(20, 20, 1)  # grid size
        grid.setSpacing(1, 1, 1)
        self.view.addItem(grid)

        self.vectors = []
        self.planes = []
        self.vector_data = []

    def add_custom_vector(self):
        try:
            vector_text = self.vector_input.text()
            vector_parts = [s.strip() for s in vector_text.split(",")]
            if len(vector_parts) != 3:
                raise ValueError("Invalid vector input!")

            x, y, z = map(float, vector_parts)
            color = (0, 1, 0, 1)  # Green
            arrow = gl.GLLinePlotItem(
                pos=np.array([[0, 0, 0], [x, y, z]]),
                color=color,
                width=3,
                mode='lines'
            )
            self.view.addItem(arrow)
            self.vectors.append(arrow)
            self.vector_data.append([x, y, z])
            self.update_display()
            self.error_label.setText("")  # Clear error message
            self.vector_input.clear()
        except ValueError:
            self.error_label.setText("Invalid vector input!")

    def add_random_vector(self):
        vec = np.random.randint(-10, 11, size=3)  # 11 is exclusive, so it covers up to 10
        color = (1, 0, 0, 1)  # Red

        arrow = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], vec]),
            color=color,
            width=3,
            mode='lines'
        )
        self.view.addItem(arrow)
        self.vectors.append(arrow)
        self.vector_data.append(vec)
        self.update_display()

    def add_random_plane(self):
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        x, y = np.meshgrid(x, y)
        z = np.zeros_like(x)  # Plane at z=0

        pts = np.vstack((x.ravel(), y.ravel(), z.ravel())).T
        mesh = gl.GLScatterPlotItem(pos=pts, color=(0, 0, 1, 0.3), size=2)
        self.view.addItem(mesh)
        self.planes.append(mesh)
        self.update_display()

    def update_display(self):
        text = "Vectors:\n"
        is_parametric = self.toggle_format_btn.isChecked()

        for i, vec in enumerate(self.vector_data):
            if is_parametric:
                text += f"v{i}: (0,0,0) + t({format_number(vec[0])}, {format_number(vec[1])}, {format_number(vec[2])})\n"
            else:
                text += f"v{i}: ({format_number(vec[0])}, {format_number(vec[1])}, {format_number(vec[2])})"
                # magnitude (length):
                magnitude = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
                text += f" | m = {format_number(magnitude)}\n"

        self.display_label.setText(text)


def format_number(num):
    # Convert the number to a string with 2 decimal places
    num_str = f"{num:.2f}"
    # Remove trailing zeros and the decimal point if unnecessary
    return num_str.rstrip('0').rstrip('.') if '.' in num_str else num_str


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VectorPlot3D()
    window.show()
    sys.exit(app.exec())
