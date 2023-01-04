from .ocv_soc_entry import OcvSocEntry
from Backend.Abstract.Model.abc_data import AbcData

class OcvSocCellData(AbcData[OcvSocEntry]):

    def __init__(self, filename: str) -> None:
        super().__init__(filename)
    
    def addEntry(self, entry: OcvSocEntry):
        self._data.append(entry)

    def add_values(self, voltage: float, soc: float) -> None:
        self._data.append(OcvSocEntry(voltage, soc))
    
