from typing import List
from PySide6.QtCore import QModelIndex

from Backend.Abstract.ViewModel.abc_vmData import AbcDataViewModel, AbcCellData
from Backend.OcvSoc.Model.ocv_soc_cellData import OcvSocCellData

class OcvSocDataViewModel(AbcDataViewModel[OcvSocCellData]):
    
    def __init__(self, data: List[OcvSocCellData]) -> None:
        super().__init__(data)

    def addData(self, data: AbcCellData) -> bool:
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._dataObjects.append(data)
        self.endInsertRows()
        self.celldataChanged.emit(self._dataObjects)
        self.selectedValueChanged.emit()

    def removeData(self, index: int):
        self.beginRemoveRows(QModelIndex(), index, index)
        del self._dataObjects[index]
        self.endRemoveRows()
        self.celldataChanged.emit(self._dataObjects)

    def getData(self, filepath: str) -> OcvSocCellData:
        for i in range(len(self._dataObjects)):
            if (self._dataObjects[i].fileInfo.filePath == filepath):
                return self._dataObjects[i]
        return None
