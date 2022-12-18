import sys
from route_parse import parse_routes, get_stations, shortest_path, Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QDialogButtonBox

class DropdownMenuExample(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Route Finder")

        self.Title= QLabel("Route and Fares:")
        self.Title.setFont(QFont("Arial", 18))
        self.start= QLabel("Origin:")
        self.end = QLabel("Destination:")

        stations = sorted(get_stations())
        self.menu1 = QComboBox()
        self.menu1.addItems(stations)
        self.menu2 = QComboBox()
        self.menu2.addItems(stations)

        self.button = QPushButton("Find Route")
        self.button.clicked.connect(self.show_result)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.Title)
        self.layout.addWidget(self.start)
        self.layout.addWidget(self.menu1)
        self.layout.addWidget(self.end)
        self.layout.addWidget(self.menu2)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.show()

    def show_result(self):
        self.msg = MessageBox()
        from_station = self.menu1.currentText()
        to_station = self.menu2.currentText()
        self.msg.setWindowTitle(f"{from_station} ➣ {to_station}")
        res = ""
        path = shortest_path(from_station, to_station)
        if path.path is None:
            res += f"No path found from {from_station} to {to_station}"
            return
        for i in range(len(path.path) - 1):
            from_station = f"{path.path[i].name} (Origin, {path.path[0].type.upper()})" if i == 0 else path.path[i].name
            if path.path[i].type != path.path[i+1].type:
                res += f"{from_station} ➣(Interchange ⟳ to {path.path[i+1].type.upper()})➣ "
            else:
                res += f"{from_station} ➣ "
        res += f"{path.path[len(path.path)-1].name} (Destination)\n"
        res += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        res += f"Approximate Time: {path.time} minutes\n"
        res += f"Approximate Cost: {path.cost} baht\n"
        res += f"Number of Stops: {path.stops}\n"
        self.msg.setText(res)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

class MessageBox(QMessageBox, QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid_layout = self.layout()

        qt_msgboxex_icon_label = self.findChild(QLabel, "qt_msgboxex_icon_label")
        qt_msgboxex_icon_label.deleteLater()

        qt_msgbox_label = self.findChild(QLabel, "qt_msgbox_label")
        qt_msgbox_label.setAlignment(Qt.AlignCenter)
        grid_layout.removeWidget(qt_msgbox_label)

        qt_msgbox_buttonbox = self.findChild(QDialogButtonBox, "qt_msgbox_buttonbox")
        grid_layout.removeWidget(qt_msgbox_buttonbox)

        grid_layout.addWidget(qt_msgbox_label, 0, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(qt_msgbox_buttonbox, 1, 0, alignment=Qt.AlignCenter)

parse_routes()
app = QApplication(sys.argv)
window = DropdownMenuExample()
sys.exit(app.exec_())