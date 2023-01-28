from PySide6.QtCore import Signal

from ...Abstract.Model.abc_data import AbcData
from ...Abstract.ViewModel.abc_vmBase import AbcVmGraphViewAll

class OcvSocCellDataGraph(AbcVmGraphViewAll):

    seriesAdded = Signal(AbcData)
    seriesRemoved = Signal(AbcData)

    def __init__(self) -> None:
        super().__init__()

    def _addData(self, data: AbcData):
        self.seriesAdded.emit(data)

    def _removeData(self, data: AbcData):
        self.seriesRemoved.emit(data)