import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt


class AnimationThread(QThread):
    update_signal = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.xdata = np.linspace(0, 10, 100)
        self.ydata = np.sin(self.xdata)
        self.animation = None

    def run(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        axes = fig.add_subplot(111)
        (line,) = axes.plot([], [], "b-")

        def update_plot(frame):
            line.set_data(self.xdata[:frame], self.ydata[:frame])
            canvas.draw()
            image = np.frombuffer(canvas.tostring_rgb(), dtype="uint8")
            image = image.reshape(canvas.get_width_height()[::-1] + (3,))
            self.update_signal.emit(image)

        self.animation = animation.FuncAnimation(fig, update_plot, frames=100, interval=50, init_func=None)
        plt.show(block=False)

    def stop_animation(self):
        if self.animation is not None:
            self.animation.event_source.stop()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)

        self.axes = self.figure.add_subplot(111)
        self.image = self.axes.imshow(np.zeros((1, 1, 3), dtype=np.uint8))

        self.animation_thread = None

        self.button_start = QPushButton("Start Animation")
        self.button_start.clicked.connect(self.start_animation)

        self.button_stop = QPushButton("Stop Animation")
        self.button_stop.clicked.connect(self.stop_animation)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_stop)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def start_animation(self):
        if self.animation_thread is None:
            self.animation_thread = AnimationThread()
            self.animation_thread.update_signal.connect(self.update_plot)
            self.animation_thread.start()

    def stop_animation(self):
        if self.animation_thread is not None:
            self.animation_thread.stop_animation()
            self.animation_thread.quit()
            self.animation_thread.wait()
            self.animation_thread = None

    def update_plot(self, image):
        self.image.set_data(image)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
