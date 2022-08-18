import sys
import numpy as np

from typing import List, TypeVar, Generic, Union
from PySide6.QtCore import Property, Signal, QPointF, QModelIndex, QPersistentModelIndex, Slot, QEnum, QObject, QAbstractTableModel
from PySide6.QtCharts import QAbstractSeries
from .abc_celldata import AbcCellData
from .abc_entry import AbcEntry

T = TypeVar("T")

class AbcCellDataGraph(QObject, Generic[T]):

    minXChanged = Signal(float)
    maxXChanged = Signal(float)
    minYChanged = Signal(float)
    maxYChanged = Signal(float)

    seriesAdded = Signal(AbcCellData)
    seriesRemoved = Signal(AbcCellData)
    seriesCleared = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cellData = []
        self._minX = 0
        self._maxX = 0
        self._minY = 0
        self._maxY = 0

    def minX(self) -> float:
        return self._minX

    def minX(self, value: float):
        self._minX = value
        self.minXChanged.emit(value)

    def maxX(self) -> float:
        return self._maxX

    def maxX(self, value: float):
        self._maxX = value
        self.maxXChanged.emit(value)

    def minY(self) -> float:
        return self._minY

    def minY(self, value: float):
        self._minY = value
        self.minYChanged.emit(value)

    def maxY(self) -> float:
        return self._maxY

    def maxY(self, value: float):
        self._maxY = value
        self.maxYChanged.emit(value)

    def addCellData(self, cellData: AbcCellData):
        self._cellData.append(cellData)
        #self._updateMinMax()
        self.seriesAdded.emit(cellData)

    def removeCellData(self, cellData: AbcCellData):
        self._cellData.remove(cellData)
        #self._updateMinMax()
        self.seriesRemoved.emit(cellData)

    def clearCellData(self):
        self._cellData.clear()
        #self._updateMinMax()
        self.seriesCleared.emit()

    def _updateMinMax(self):

        if (len(self._cellData) == 0):
            self._resetMinMax()

        for i in range(len(self._cellData)):
            cd = AbcCellData(self._cellData[i])
            minP = AbcEntry(cd.data[0]).getPoint()
            maxP = AbcEntry(cd.data[len(cd.data)]).getPoint()
            if (minP.x < self.minX):
                self.minX = minP.x
            if (minP.y < self.minY):
                self.minY = minP.y
            if (maxP.x < self.maxX):
                self.maxX = maxP.x
            if (maxP.y < self.maxY):
                self.maxY = maxP.y

    def _resetMinMax(self):
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
