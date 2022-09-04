from typing import TypeVar, Generic
from PySide6.QtCore import Signal, QObject, Slot, Property

from .abc_vmBase import AbcVmBaseViewAll
from .abc_vmData import AbcDataViewModel, AbcCellData

T = TypeVar("T", bound=AbcDataViewModel)

class AbcCellDataGraph(AbcVmBaseViewAll, QObject, Generic[T]):

    # Signals for connection in qml GraphView
    seriesAdded = Signal(AbcCellData)
    seriesRemoved = Signal(AbcCellData)
    seriesCleared = Signal()

    def __init__(self, model: T):
        super().__init__(model)

    # View all implementation

    def onViewAllChanging(self):
        self.viewAllChanged.emit(self._viewAll)

    # Update slots

    @Slot()
    def onDataChanged(self):
        if self._model.canUpdateView():
            if self._viewAll:
                self.updateAll()
            else:
                self.updateSelection()

    @Slot()
    def onSelectionChanged(self):
        if self._model.canUpdateView():
            if not self._viewAll:
                self.updateSelection()
    
    @Slot()
    def clear(self):
        self.seriesCleared.emit()

    def updateAll(self):
        self.seriesCleared.emit()
        for i in range(len(self._model.dataObjects)):
            self.seriesAdded.emit(self._model.dataObjects[i])

    def updateSelection(self):
        if (self._model.selectedIndex >= 0 and self._model.selectedIndex < len(self._model.dataObjects)):
            selected = self._model.dataObjects[self._model.selectedIndex]
            if (selected is not None):
                self.seriesCleared.emit()
                self.seriesAdded.emit(selected)
