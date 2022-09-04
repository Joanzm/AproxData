from PySide6.QtCore import Qt, Signal, QModelIndex, QPersistentModelIndex, Slot, QAbstractTableModel
from abc import abstractmethod
from typing import List, TypeVar, Generic, Union

from .abc_vmBase import AbcVmBaseViewAll
from .abc_vmData import AbcDataViewModel, AbcCellData

T = TypeVar("T", bound=AbcDataViewModel)

class AbcCellDataTable(AbcVmBaseViewAll, QAbstractTableModel, Generic[T]):

    dataChanged = Signal('QVariantList')
    headerDataChanged = Signal(Qt.Orientation, int, int)

    def __init__(self, model: T) -> None:
        super().__init__(model)
        self._isHeaderVisible = True
        self._data = []
        self._headers = ["Soc", "Voltage"]

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
        self.clearEntries()

    def updateAll(self):
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, self.columnCount(None) - 1)
        self.clearEntries()
        entries = self._model.listAllData()
        self._headers = entries.pop(0)
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(entries) - 1))
        self._data = entries
        self.endInsertRows()
        self.dataChanged.emit(self._data)

    def updateSelection(self):
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, self.columnCount(None) - 1)
        if (self._model.selectedIndex >= 0 and self._model.selectedIndex < len(self._model.dataObjects)):
            selected = self._model.dataObjects[self._model.selectedIndex]
            if (selected is not None):
                self.clearEntries()
                self._headers = ["Soc", "Voltage"]
                self.addEntries(selected)

    @Slot(int, Qt.Orientation, result="QVariant")
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if (role == Qt.DisplayRole and orientation == Qt.Orientation.Horizontal):
            return self._headers[section]

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

    def addEntries(self, obj: AbcCellData):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(obj.data) - 1))
        for i in range(len(obj.data)):
            self._data.append(obj.data[i])
        self.endInsertRows()
        self.dataChanged.emit(self._data)

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
