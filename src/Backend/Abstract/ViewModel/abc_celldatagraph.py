from typing import TypeVar, Generic
from PySide6.QtCore import Signal, QObject, Slot

from ..Model.abc_model import AbcModel, AbcCellData

T = TypeVar("T", bound=AbcModel)
W = TypeVar("W", bound=AbcCellData)

class AbcCellDataGraph(QObject, Generic[T,W]):

    seriesAdded = Signal(AbcCellData)
    seriesRemoved = Signal(AbcCellData)
    seriesCleared = Signal()

    def __init__(self, model: T):
        super().__init__()
        self._model = model
        self._cellData = []
        self._model.updateSignal.connect(self.updateGraph)
        self._model.clearSignal.connect(self.clearGraph)

    # Update slots

    @Slot()
    def updateGraph(self):
        if (self._model.selectedIndex >= 0 and self._model.selectedIndex < len(self._model.dataObjects)):
            selected = self._model.dataObjects[self._model.selectedIndex]
            if (selected is not None):
                self.seriesCleared.emit()
                self.seriesAdded.emit(selected)

    @Slot()
    def clearGraph(self):
        self.seriesCleared.emit()
        
