from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

from PySide6.QtCore import Qt, Property, Signal, QAbstractListModel, QModelIndex, QObject

from Model.Abstract.abc_celldata import AbcCellData

T = TypeVar("T")

class AbcModel(QAbstractListModel, Generic[T]):

    celldataChanged = Signal('QVariantList')
    selectedIndexChanged = Signal(int)
    selectedValueChanged = Signal()

    def __init__(self, data: List[T]) -> None:
        super().__init__()
        self._selectedIndex = -1
        self._dataObjects = data
    
    # QAbstractListModel implementation

    cellDataRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            AbcModel.cellDataRole: b'celldata',
        }

    def rowCount(self, parent=QModelIndex()):
       return len(self._dataObjects)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == AbcModel.cellDataRole:
                return self._dataObjects[index.row()]
        return None

    # Selection implementation

    @Property(int, notify=selectedIndexChanged)
    def selectedIndex(self) -> int:
        return self._selectedIndex
    
    @selectedIndex.setter
    def selectedIndex(self, value: int):
        if (self._selectedIndex != value):
            self._selectedIndex = value
            self.selectedIndexChanged.emit(value)
            self.selectedValueChanged.emit()

    @Property(QObject, notify=selectedValueChanged)
    def selectedValue(self) -> AbcCellData:
        if (self._selectedIndex < 0 or self._selectedIndex > len(self._dataObjects) - 1):
            return None
        else:
            return self._dataObjects[self._selectedIndex]

    # Model properties and functions

    @Property('QVariantList', notify=celldataChanged)
    def dataObjects(self) -> List[T]:
        return self._dataObjects

    @dataObjects.deleter
    def dataObjects(self):
        self._dataObjects = []

    # ABSTRACT

    @abstractmethod
    def removeData(self, index: int):
        pass

    @abstractmethod
    def addData(self, data: AbcCellData) -> bool:
        pass


