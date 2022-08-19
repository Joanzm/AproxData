from PySide6.QtCore import Qt, QModelIndex, QPersistentModelIndex
from typing import Union

from .ocv_soc_vmData import OcvSocDataViewModel, OcvSocCellData
from Backend.Abstract.ViewModel.abc_vmCellDataTable import AbcCellDataTable

class OcvSocCellDataTable(AbcCellDataTable[OcvSocDataViewModel, OcvSocCellData]):

    def __init__(self, model: OcvSocDataViewModel) -> None:
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
    
