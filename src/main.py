import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterType
from Backend.Abstract.Model.abc_celldata import AbcCellData
from Backend.OcvSoc.Model.ocv_soc_celldata import OcvSocCellData
from Backend.OcvSoc.Model.ocv_soc_entry import OcvSocEntry
from Backend.main_model import CellDataAnalyzerModel

if __name__ == "__main__":
    """
    Starts the tkinter GUI
    """
    app = QApplication(sys.argv)
    qmlRegisterType(CellDataAnalyzerModel, 'CellDataAnalyzerModel', 1, 0, 'CellDataAnalyzerModel')
    qmlRegisterType(AbcCellData, 'AbcCellData', 1, 0, 'AbcCellData')
    qmlRegisterType(OcvSocCellData, 'OcvSocCellData', 1, 0, 'OcvSocCellData')
    qmlRegisterType(OcvSocEntry, 'CellEntries', 1, 0, 'OcvSocEntry')

    engine = QQmlApplicationEngine()
    engine.load("src/View/Main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())