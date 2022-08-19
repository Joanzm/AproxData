from typing import List
from PySide6.QtCore import Property, Signal, QObject

from .OcvSoc.ViewModel.ocv_soc_vmData import OcvSocDataViewModel

from .OcvSoc.Model.ocv_soc_cellData import OcvSocCellData
from .OcvSoc.ViewModel.ocv_soc_vmCellDataTable import OcvSocCellDataTable
from .OcvSoc.ViewModel.ocv_soc_vmCellDataGraph import OcvSocCellDataGraph
from .OcvSoc.ocv_soc_runnable import OcvSocLoadXlsFileRunner

class CellDataAnalyzerModel(QObject):

    titleChanged = Signal(str)

    vmChanged = Signal(QObject)
    vmDataTableChanged = Signal(QObject)
    vmDataGraphChanged = Signal(QObject)
    loadFileRunnerChanged = Signal(QObject)

    def __init__(self) -> None:
        super().__init__()
        self._title = ""
        self._model = OcvSocDataViewModel([])
        self._dataParser = OcvSocLoadXlsFileRunner(self._model)
        self._cellDataTable = OcvSocCellDataTable(self._model)
        self._cellDataGraph = OcvSocCellDataGraph(self._model)
        self.vmDataGraphChanged.emit(self._cellDataGraph)

    # Title of this model class

    @Property(str, notify=titleChanged)
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value
        self.titleChanged.emit(value)

    # Cell data model

    @Property(QObject, notify=vmChanged)
    def model(self):
        return self._model

    @property
    def data(self) -> List[OcvSocCellData]:
        return self._model.dataObjects

    @property
    def selectedIndex(self):
        return self._model.selectedIndex

    # Table view reference and update mehtods

    @Property(QObject, notify=vmDataTableChanged)
    def cellDataTable(self):
        return self._cellDataTable

    # Graph view reference and update methods

    @Property(QObject, notify=vmDataGraphChanged)
    def cellDataGraph(self):
        return self._cellDataGraph

    # Load file instance

    @Property(QObject, notify=loadFileRunnerChanged)
    def dataParser(self):
        return self._dataParser

    