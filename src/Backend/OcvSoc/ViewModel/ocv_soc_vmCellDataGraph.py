from PySide6.QtCore import Signal

from Backend.Abstract.Model.abc_data import AbcData
from Backend.Abstract.ViewModel.abc_vmBase import AbcGraph

class OcvSocCellDataGraph(AbcGraph):

    seriesAdded = Signal(AbcData)
    seriesRemoved = Signal(AbcData)

    def __init__(self) -> None:
        super().__init__()

    def _addSeries(self, data: AbcData):
        self.seriesAdded.emit(data)

    def _removeSeries(self, data: AbcData):
        self.seriesRemoved.emit(data)