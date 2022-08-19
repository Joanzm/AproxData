from PySide6.QtCore import Property, Signal, QModelIndex, QPersistentModelIndex, Slot, QAbstractTableModel
from abc import abstractmethod
from typing import List, TypeVar, Generic, Union

from ..Model.abc_model import AbcModel, AbcCellData

T = TypeVar("T", bound=AbcModel)
W = TypeVar("W", bound=AbcCellData)

class AbcCellDataTable(QAbstractTableModel, Generic[T, W]):

    currIndexChanged = Signal(int)
    dataChanged = Signal('QVariantList')

    def __init__(self, model: T) -> None:
        super().__init__()
        self._data = []
        self._model = model
        self._model.updateSignal.connect(self.updateTable)
        self._model.clearSignal.connect(self.clearTable)

    # Update slots

    @Slot()
    def updateTable(self):
        if (self._model.selectedIndex >= 0 and self._model.selectedIndex < len(self._model.dataObjects)):
            selected = self._model.dataObjects[self._model.selectedIndex]
            if (selected is not None):
                if (selected.dataLength() > 0):
                    self.resetEntries(selected)
                else:
                    self.clearEntries()

    @Slot()
    def clearTable(self):
        self.clearEntries()

    # QAbstractTableModel implementation

    def rowCount(self, parent=QModelIndex()):
       return len(self._data)

    @abstractmethod
    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        pass

    @abstractmethod
    def data(self, index, role):
        pass

    @abstractmethod
    def roleNames(self):
        pass

    # Manipulate data implementation

    @abstractmethod
    def addEntries(self, obj: W):
        pass

    @abstractmethod
    def resetEntries(self, obj: W):
        pass

    @Slot(int)
    def deleteEntry(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
        self.dataChanged.emit(self._data)

    def clearEntries(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data) - 1)
        self._data.clear()
        self.endRemoveRows()
        self.dataChanged.emit(self._data)

