from PySide6.QtCore import Qt, QModelIndex, QPersistentModelIndex
from typing import Union

from .ocv_soc_vmData import OcvSocDataViewModel
from Backend.Abstract.ViewModel.abc_vmCellDataTable import AbcCellDataTable

class OcvSocCellDataTable(AbcCellDataTable[OcvSocDataViewModel]):

    def __init__(self, model: OcvSocDataViewModel) -> None:
        super().__init__(model)

    # QAbstractTableModel implementation

    displayRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            OcvSocCellDataTable.displayRole: b'display'
        }

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        if len(self._data) > 0:
            if self._viewAll:
                return len(self._model.dataObjects) + 2
            else:
                return 2
        else:
            return 0

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == OcvSocCellDataTable.displayRole:
                if self._viewAll:
                    return self._data[index.row()][index.column()]
                else:
                    if (index.column() == 0):
                        return self._data[index.row()].soc
                    elif (index.column() == 1):
                        return self._data[index.row()].voltage
        return None
