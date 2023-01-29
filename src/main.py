import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterType

from Core.main_vm import CellDataAnalyzerViewModel, QDatasetList, QDataTable, QDataGraph, AbcVmInterpolation
from Core.Model.aprox_data import DataSet, DataEntry

if __name__ == "__main__":
    """
    Starts the QT GUI via PySide6
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("src/View/AproxIcon.ico"))

    qmlRegisterType(CellDataAnalyzerViewModel, 'CellDataAnalyzerViewModel', 1, 0, 'CellDataAnalyzerViewModel')
    qmlRegisterType(QDatasetList, 'QDatasetList', 1, 0, 'QDatasetList')
    qmlRegisterType(QDataTable, 'QDataTable', 1, 0, 'QDataTable')
    qmlRegisterType(QDataGraph, 'QDataGraph', 1, 0, 'QDataGraph')
    qmlRegisterType(AbcVmInterpolation, 'AbcVmInterpolation', 1, 0, 'AbcVmInterpolation')

    engine = QQmlApplicationEngine()
    engine.load("src/View/Main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())