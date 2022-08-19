from typing import TypeVar, Generic
from PySide6.QtCore import Signal, QObject, Slot, Property

from .abc_vmData import AbcDataViewModel, AbcCellData

T = TypeVar("T", bound=AbcDataViewModel)
W = TypeVar("W", bound=AbcCellData)

class AbcCellDataGraph(QObject, Generic[T,W]):

    # Signals for connection in qml GraphView
    seriesAdded = Signal(AbcCellData)
    seriesRemoved = Signal(AbcCellData)
    seriesCleared = Signal()
    # Property signals
    viewAllChanged = Signal(bool)

    def __init__(self, model: T):
        super().__init__()
        self._model = model
        self._viewAll = False
        self._model.updateGraphSignal.connect(self.updateGraph)
        self._model.clearGraphSignal.connect(self.clearGraph)

    # Update slots

    @Slot()
    def updateGraph(self):
        if self._model.canUpdateView():
            if self._viewAll:
                self.seriesCleared.emit()
                for i in range(len(self._model.dataObjects)):
                    self.seriesAdded.emit(self._model.dataObjects[i])
            else:
                if (self._model.selectedIndex >= 0 and self._model.selectedIndex < len(self._model.dataObjects)):
                    selected = self._model.dataObjects[self._model.selectedIndex]
                    if (selected is not None):
                        self.seriesCleared.emit()
                        self.seriesAdded.emit(selected)

    @Slot()
    def clearGraph(self):
        self.seriesCleared.emit()

    # View model properties

    @Property(bool, notify=viewAllChanged)
    def viewAll(self) -> bool:
        return self._viewAll

    @viewAll.setter
    def viewAll(self, value: bool):
        self._viewAll = value
        self.viewAllChanged.emit(value)
        self.updateGraph()
        
