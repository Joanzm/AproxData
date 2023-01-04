import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterType

from Backend.main_vm import CellDataAnalyzerViewModel, OcvSocDataListViewModel, OcvSocCellDataTable, OcvSocCellDataGraph, OcvSocInterpolation

from Backend.Abstract.Model.abc_data import AbcData
from Backend.OcvSoc.Model.ocv_soc_celldata import OcvSocCellData
from Backend.OcvSoc.Model.ocv_soc_entry import OcvSocEntry

if __name__ == "__main__":
    """
    Starts the QT GUI via PySide6
    """
    app = QApplication(sys.argv)
    qmlRegisterType(CellDataAnalyzerViewModel, 'CellDataAnalyzerViewModel', 1, 0, 'CellDataAnalyzerViewModel')
    qmlRegisterType(OcvSocDataListViewModel, 'OcvSocDataListViewModel', 1, 0, 'OcvSocDataListViewModel')
    qmlRegisterType(OcvSocCellDataTable, 'OcvSocCellDataTable', 1, 0, 'OcvSocCellDataTable')
    qmlRegisterType(OcvSocCellDataGraph, 'OcvSocCellDataGraph', 1, 0, 'OcvSocCellDataGraph')
    qmlRegisterType(OcvSocInterpolation, 'OcvSocInterpolation', 1, 0, 'OcvSocInterpolation')
    qmlRegisterType(OcvSocCellData, 'OcvSocCellData', 1, 0, 'OcvSocCellData')
    qmlRegisterType(AbcData, 'AbcData', 1, 0, 'AbcData')
    qmlRegisterType(OcvSocEntry, 'CellEntries', 1, 0, 'OcvSocEntry')

    engine = QQmlApplicationEngine()
    engine.load("src/View/Main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())