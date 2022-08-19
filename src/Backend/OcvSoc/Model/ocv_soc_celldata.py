from .ocv_soc_entry import OcvSocEntry
from Backend.Abstract.Model.abc_cellData import AbcCellData

class OcvSocCellData(AbcCellData[OcvSocEntry]):

    def __init__(self, filename: str) -> None:
        super().__init__(filename)
    
    def addEntry(self, entry: OcvSocEntry):
        self._celldata.append(entry)

    def add_values(self, voltage: float, soc: float) -> None:
        self._celldata.append(OcvSocEntry(voltage, soc))
    
