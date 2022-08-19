from typing import TypeVar, Generic
from PySide6.QtCore import Signal, QObject
from .abc_celldata import AbcCellData

T = TypeVar("T")

class AbcCellDataGraph(QObject, Generic[T]):

    seriesAdded = Signal(AbcCellData)
    seriesRemoved = Signal(AbcCellData)
    seriesCleared = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cellData = []

    def addCellData(self, cellData: AbcCellData):
        self._cellData.append(cellData)
        self.seriesAdded.emit(cellData)

    def removeCellData(self, cellData: AbcCellData):
        self._cellData.remove(cellData)
        self.seriesRemoved.emit(cellData)

    def clearCellData(self):
        self._cellData.clear()
        self.seriesCleared.emit()
