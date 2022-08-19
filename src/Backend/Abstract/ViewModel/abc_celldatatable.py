from PySide6.QtCore import Property, Signal, QModelIndex, QPersistentModelIndex, Slot, QAbstractTableModel
from abc import abstractmethod
from typing import List, TypeVar, Generic, Union

T = TypeVar("T")

class AbcCellDataView(QAbstractTableModel, Generic[T]):

    currIndexChanged = Signal(int)
    dataChanged = Signal('QVariantList')

    def __init__(self, currindex: int, data: List[type[T]] = []) -> None:
        super().__init__()
        self._currindex = currindex
        self._data = data

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
    def addEntries(self, entries: List[type[T]]):
        pass

    @abstractmethod
    def resetEntries(self, entries: List[type[T]]):
        pass

    @Slot(int)
    def delete_entry(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
        self.dataChanged.emit(self._data)

    def clear_entries(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data) - 1)
        self._data.clear()
        self.endRemoveRows()
        self.dataChanged.emit(self._data)

    # Displaying index

    @Property(int, notify=currIndexChanged)
    def currindex(self) -> int:
        return self._currindex

    @currindex.setter
    def currindex(self, value: int):
        self._currindex = value
        self.currIndexChanged.emit(value)

