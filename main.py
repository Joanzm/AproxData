import sys
from PySide6.QtCore import QCoreApplication, Qt, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import qmlRegisterType
from Model.Abstract.abc_celldata import AbcCellData
from Model.OcvSoc.ocv_soc_celldata import OcvSocCellData
from Model.OcvSoc.ocv_soc_entry import OcvSocEntry
from Model.main_model import CellDataAnalyzerModel

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# from matplotlib.figure import Figure

# class MplCanvas(FigureCanvasQTAgg):

#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)

# class MainWindow(QMainWindow):

#     def __init__(self, *args, **kwargs) -> None:
#         super(MainWindow, self).__init__(*args, **kwargs)

#         # Create the maptlotlib FigureCanvas object,
#         # which defines a single set of axes as self.axes.
#         sc = MplCanvas(self, width=5, height=4, dpi=100)
#         sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
#         self.setCentralWidget(sc)
        
#         dock = QDockWidget("Graph", self)
#         dock.setAllowedAreas(Qt.BottomDockWidgetArea)
#         view = QQuickWidget()
#         view.setSource("View/Main.qml")
#         dock.setWidget(view)
#         self.addDockWidget(dock, Qt.BottomDockWidgetArea)
        
#         self.show()

if __name__ == "__main__":
    """
    Starts the tkinter GUI
    """
    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    qmlRegisterType(CellDataAnalyzerModel, 'CellDataAnalyzerModel', 1, 0, 'CellDataAnalyzerModel')
    qmlRegisterType(AbcCellData, 'AbcCellData', 1, 0, 'AbcCellData')
    qmlRegisterType(OcvSocCellData, 'OcvSocCellData', 1, 0, 'OcvSocCellData')
    qmlRegisterType(OcvSocEntry, 'CellEntries', 1, 0, 'OcvSocEntry')
    # qmlRegisterType(FigureCanvasQTAgg, "Graphing", 1, 0, "FigureCanvas")

    engine = QQmlApplicationEngine()
    engine.load("View/Main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())