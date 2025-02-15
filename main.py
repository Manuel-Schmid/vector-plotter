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

        self.position_input = QLineEdit()
        self.vector_input = QLineEdit()
        self.vector_input.returnPressed.connect(self.add_custom_vector)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")

        self.add_custom_vector_btn = QPushButton("Plot Custom Vector")
        self.add_custom_vector_btn.clicked.connect(self.add_custom_vector)
        self.add_random_vector_btn = QPushButton("Add Random Vector")
        self.add_random_vector_btn.clicked.connect(self.add_random_vector)

        settings_layout.addRow(QLabel("Enter Position Vector (x, y, z):"), self.position_input)
        settings_layout.addRow(QLabel("Enter Direction Vector (x, y, z):"), self.vector_input)
        settings_layout.addRow(self.error_label)
        settings_layout.addRow(self.add_custom_vector_btn)
        settings_layout.addRow(self.add_random_vector_btn)

        # Toggle Format Button
        self.toggle_format_btn = QCheckBox("Parameter Form")
        self.toggle_format_btn.stateChanged.connect(self.update_display)
        settings_layout.addRow(self.toggle_format_btn)

        # Display Vectors
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
        self.vector_data = []

    def add_custom_vector(self):
        try:
            pos_text = self.position_input.text()
            vec_text = self.vector_input.text()

            pos_parts = [s.strip() for s in pos_text.split(",")]
            vec_parts = [s.strip() for s in vec_text.split(",")]
            if len(vec_parts) != 3:
                raise ValueError("Invalid vector input!")

            if len(pos_parts) == 3:
                px, py, pz = map(float, pos_parts)
            else:
                px, py, pz = 0,0,0
            vx, vy, vz = map(float, vec_parts)

            color = (0, 1, 0, 1)  # Green
            arrow = gl.GLLinePlotItem(
                pos=np.array([[px, py, pz], [px + vx, py + vy, pz + vz]]),
                color=color,
                width=3,
                mode='lines'
            )
            self.view.addItem(arrow)
            self.vectors.append(arrow)
            self.vector_data.append(((px, py, pz), (vx, vy, vz)))
            self.update_display()
            self.error_label.setText("")  # Clear error message
            self.vector_input.clear()
            self.position_input.clear()
        except ValueError:
            self.error_label.setText("Invalid vector input!")

    def add_random_vector(self):
        px, py, pz = np.random.randint(-5, 6, size=3)
        vx, vy, vz = np.random.randint(-10, 11, size=3) # 11 is exclusive, so it covers up to 10
        color = (1, 0, 0, 1)  # Red

        arrow = gl.GLLinePlotItem(
            pos=np.array([[px, py, pz], [px + vx, py + vy, pz + vz]]),
            color=color,
            width=3,
            mode='lines'
        )
        self.view.addItem(arrow)
        self.vectors.append(arrow)
        self.vector_data.append(((px, py, pz), (vx, vy, vz)))
        self.update_display()

    def update_display(self):
        text = "Vectors:\n"
        is_parametric = self.toggle_format_btn.isChecked()

        for i, (pos, vec) in enumerate(self.vector_data):
            px, py, pz = pos
            vx, vy, vz = vec
            if is_parametric:
                text += f"v{i}: ({px},{py},{pz}) + t({format_number(vx)}, {format_number(vy)}, {format_number(vz)})\n"
            else:
                text += f"v{i}: ({px},{py},{pz}) + t({format_number(vx)}, {format_number(vy)}, {format_number(vz)})"
                # magnitude (length):
                magnitude = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
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
