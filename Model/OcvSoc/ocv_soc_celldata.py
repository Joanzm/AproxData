from PySide6.QtCore import Qt, Slot, QModelIndex, QPersistentModelIndex, Signal
from typing import List, Union
from .ocv_soc_entry import OcvSocEntry
from Model.Abstract.abc_celldata import AbcCellData, ProcessState

class OcvSocCellData(AbcCellData[OcvSocEntry]):

    def __init__(self, filename: str) -> None:
        super().__init__(filename)

    @Slot(OcvSocEntry)
    def addEntry(self, entry: OcvSocEntry):
        self._celldata.append(entry)

    def add_values(self, voltage: float, soc: float) -> None:
        self._celldata.append(OcvSocEntry(voltage, soc))
    
