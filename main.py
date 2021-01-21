from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from numpy import *
import sys

matplotlib.use('Qt5Agg')

# Canvas for graph embedding
# ============================
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

# Main app class
# =======================
class MyAPP(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.create_app()

    def create_app(self):

        # Setting GUI
        # ======================================
        self.grid = QGridLayout()

        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        self.errors = QLabel()
        self.errors.setMaximumHeight(23)
        self.errors.setFont(QFont("Arial", 12))
        self.errors.setAlignment(Qt.AlignCenter)
        label1 = QLabel("Enter function (in terms of x)")
        self.input1 = QLineEdit()
        self.input1.setFixedHeight(30)
        label2 = QLabel("Min value of x")
        self.input2 = QLineEdit()
        self.input2.setFixedHeight(30)
        label3 = QLabel("Max value of x")
        self.input3 = QLineEdit()
        self.input3.setFixedHeight(30)
        submit_btn = QPushButton("Submit")

        submit_btn.clicked.connect(self.plotting)
        self.grid.addWidget(self.errors, 0, 0, 1, 2)
        self.grid.addWidget(label1, 1, 0, 1, 1)
        self.grid.addWidget(self.input1, 1, 1, 1, 1)
        self.grid.addWidget(label2, 2, 0, 1, 1)
        self.grid.addWidget(self.input2, 2, 1, 1, 1)
        self.grid.addWidget(label3, 3, 0, 1, 1)
        self.grid.addWidget(self.input3, 3, 1, 1, 1)
        self.grid.addWidget(submit_btn, 4, 0, 1, 2)
        canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.grid.addWidget(canvas, 5, 0, 5, 5)
        self.setLayout(self.grid)

    # Button click handling
    # ====================================
    def plotting(self):
        max_x = str(self.input3.text())
        min_x = str(self.input2.text())
        y = str(self.input1.text())
        x = self.validate_x(min_x, max_x)
        updated_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        if x == 1:
            x = linspace(float(min_x), float(max_x), 100)
            y = self.validate_y(x, y)
            if y != -1:
                self.errors.setText("")
                updated_canvas.axes.plot(x, eval(y))
        self.grid.addWidget(updated_canvas, 5, 0, 5, 5)
        self.show()

    # Function entered validation
    # ====================================
    def validate_y(self, x, func_x):
        if func_x.find("e^") != -1:
            self.errors.setText("Exponential functions should be typed in this form: exp(input)")
            return -1
        if func_x.count('(') != func_x.count(')'):
            self.errors.setText("There is missing bracket(s)")
            return -1
        func_x = func_x.replace("^", "**")

        try:
            plt.plot(x, eval(func_x))
        except:
            self.errors.setText("Function is not expressed correctly")
            return -1
        return func_x

    # Min and max x values validation
    # ====================================
    def validate_x(self, x1, x2):
        if x2 <= x1 and x1.lstrip('-').isnumeric() and x2.lstrip('-').isnumeric():
            self.errors.setText("Invalid range for x")
            return -1
        try:
            float(x1)
            float(x2)
            return 1
        except ValueError:
            self.errors.setText("Please enter numeric values for x ranges")
            return -1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyAPP()
    window.show()
    sys.exit(app.exec_())
