from PySide6.QtCore import Qt, QObject, Signal, QModelIndex, QPersistentModelIndex, Property, Slot
from abc import abstractmethod
from typing import List, Union

from Backend.OcvSoc.Model.ocv_soc_interpolation import OcvSoc2DLinearInterpolation
from Backend.OcvSoc.Model.ocv_soc_celldata import OcvSocCellData
from Backend.Abstract.ViewModel.abc_vmBase import AbcVmTable

class OcvSocLookUpTable(QObject):

    lookUpTableChanged = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._lookUpTable = ""
        self._interpolation = OcvSoc2DLinearInterpolation()

    @Property(str, notify=lookUpTableChanged)
    def lookUpTable(self) -> str:
        return self._lookUpTable
    
    @lookUpTable.setter
    def lookUpTable(self, value: str):
        self._lookUpTable = value
        self.lookUpTableChanged.emit(value)

    Slot(list)
    def onSelectedChanged(self, data : List):
        print()