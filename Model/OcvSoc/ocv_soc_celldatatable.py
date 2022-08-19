from PySide6.QtCore import Qt, Slot, QModelIndex, QPersistentModelIndex
from typing import List, Union
from .ocv_soc_entry import OcvSocEntry
from Model.Abstract.abc_celldatatable import AbcCellDataView

class OcvSocCellDataView(AbcCellDataView[OcvSocEntry]):

    def __init__(self, index: int, data: List[type[OcvSocEntry]] = []) -> None:
        super().__init__(index, data)

    # QAbstractTableModel implementation

    displayRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            OcvSocCellDataView.displayRole: b'display'
        }

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        return 2

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == OcvSocCellDataView.displayRole:
                if (index.column() == 0):
                    return self._data[index.row()].voltage
                elif (index.column() == 1):
                    return self._data[index.row()].soc
        return None

    # Change data

    def addEntries(self, entries: List[type[OcvSocEntry]]):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(entries) - 1))
        for i in range(len(entries)):
            self._data.append(entries[i])
        self.endInsertRows()
        self.dataChanged.emit(self._data)

    def resetEntries(self, entries: List[type[OcvSocEntry]]):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data) - 1)
        self._data.clear()
        self.endRemoveRows()
        self.addEntries(entries)
    
