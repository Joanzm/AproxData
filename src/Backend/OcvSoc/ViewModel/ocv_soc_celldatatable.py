from PySide6.QtCore import Qt, Slot, QModelIndex, QPersistentModelIndex
from typing import List, Union

from ..Model.ocv_soc_model import OcvSocModel, OcvSocCellData
from ...Abstract.ViewModel.abc_celldatatable import AbcCellDataTable

class OcvSocCellDataTable(AbcCellDataTable[OcvSocModel, OcvSocCellData]):

    def __init__(self, model: OcvSocModel) -> None:
        super().__init__(model)

    # QAbstractTableModel implementation

    displayRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            OcvSocCellDataTable.displayRole: b'display'
        }

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        return 2

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == OcvSocCellDataTable.displayRole:
                if (index.column() == 0):
                    return self._data[index.row()].voltage
                elif (index.column() == 1):
                    return self._data[index.row()].soc
        return None

    # Change data

    def addEntries(self, obj: OcvSocCellData):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(obj.data) - 1))
        for i in range(len(obj.data)):
            self._data.append(obj.data[i])
        self.endInsertRows()
        self.dataChanged.emit(self._data)

    def resetEntries(self, obj: OcvSocCellData):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data) - 1)
        self._data.clear()
        self.endRemoveRows()
        self.addEntries(obj)
    
