from abc import abstractmethod
from typing import List, TypeVar, Generic
from PySide6.QtCore import Qt, Property, Signal, Slot, QAbstractListModel, QModelIndex, QObject

from ..Model.abc_data import AbcData, ProcessState

T = TypeVar("T", bound=AbcData)

class AbcDataList(QAbstractListModel, Generic[T]):

    # Notify global view

    # Notify properties
    dataChangedSignal = Signal(list, int, bool)
    selectionChangedSignal = Signal(list, int, bool)
    clearViewSignal = Signal()

    def __init__(self, data: List[T]) -> None:
        super().__init__()
        self._selectedIndex = -1
        self._dataObjects = data

    # Update View

    def canUpdateView(self) -> bool:
        for i in range(len(self._dataObjects)):
            if self._dataObjects[i].state == ProcessState.Pendeling or self._dataObjects[i].state == ProcessState.Processing:
                return False
        return True

    @Slot()
    def clearView(self):
        self.clearViewSignal.emit()

    @Slot()
    def updateView(self):
        self.dataChangedSignal.emit(self._dataObjects, self._selectedIndex, self.canUpdateView())
    
    # QAbstractListModel implementation

    cellDataRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            AbcDataList.cellDataRole: b'celldata',
        }

    def rowCount(self, parent=QModelIndex()):
       return len(self._dataObjects)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == AbcDataList.cellDataRole:
                return self._dataObjects[index.row()]
        return None

    # Selection implementation

    @Property(int, notify=selectionChangedSignal)
    def selectedIndex(self) -> int:
        return self._selectedIndex
    
    @selectedIndex.setter
    def selectedIndex(self, value: int):
        if (self._selectedIndex != value):
            self._selectedIndex = value
            self.selectionChangedSignal.emit(self._dataObjects, value, self.canUpdateView())

    @Property(QObject, notify=selectionChangedSignal)
    def selectedValue(self) -> AbcData:
        if (self._selectedIndex < 0 or self._selectedIndex > len(self._dataObjects) - 1):
            return None
        else:
            return self._dataObjects[self._selectedIndex]

    # Model properties and functions

    @property
    def dataObjects(self) -> List[T]:
        return self._dataObjects

    @Property(bool, notify=dataChangedSignal)
    def hasData(self) -> bool:
        return len(self._dataObjects) > 0

    def addData(self, data: T) -> bool:
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._dataObjects.append(data)
        self.endInsertRows()
        self.dataChangedSignal.emit(self._dataObjects, self._selectedIndex, self.canUpdateView())

    @Slot(int)
    def removeData(self, index: int):
        self.beginRemoveRows(QModelIndex(), index, index)
        del self._dataObjects[index]
        self.endRemoveRows()
        self.dataChangedSignal.emit(self._dataObjects, self._selectedIndex, self.canUpdateView())

    @Slot()
    def clearData(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._dataObjects) - 1)
        self._dataObjects = []
        self.endRemoveRows()
        self.dataChangedSignal.emit(self._dataObjects, self._selectedIndex, self.canUpdateView())

    # ABSTRACT

    @abstractmethod
    def getData(self, filepath: str) -> T:
        pass

    @abstractmethod
    def listAllData(self) -> List:
        pass


