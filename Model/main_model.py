from typing import List
from PySide6.QtCore import Qt, Property, Signal, QUrl, Slot, QThread, QAbstractListModel, QModelIndex, QObject

from Model.OcvSoc.ocv_soc_model import OcvSocModel

from .Abstract.abc_celldata import AbcCellData
from .OcvSoc.ocv_soc_celldata import OcvSocCellData
from .Abstract.abc_celldata import ProcessState
from .OcvSoc.ocv_soc_celldatatable import OcvSocCellDataView
from .OcvSoc.ocv_soc_celldatagraph import OcvSocCellDataGraph
from .OcvSoc.ocv_soc_runnable import LoadXlsFileWorker
from .OcvSoc import ocv_soc_celldataparser_xlr as Parser

class CellDataAnalyzerModel(QObject):

    COLUMNS = ('Datensaetze',)
    titleChanged = Signal(str)
    workerStateChanged = Signal()

    vmChanged = Signal(QObject)
    vmDataTableChanged = Signal(QObject)
    vmDataGraphChanged = Signal(QObject)

    def __init__(self) -> None:
        super().__init__()
        self.__worker = None
        self._title = ""
        self._model = OcvSocModel([])
        self._celldataview = OcvSocCellDataView(-1, [])
        self._cellDataGraph = OcvSocCellDataGraph()
        self._model.selectedIndexChanged.connect(self.__selectionChanged)

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

    @Slot(int)
    def __selectionChanged(self, index: int):
        self._updateDataView()
        self._updateGraphView()

    # Table view reference and update mehtods

    @Property(QObject, notify=vmDataTableChanged)
    def celldataview(self):
        return self._celldataview

    def _updateDataView(self):
        if (self.__worker.isFinished() and self.selectedIndex >= 0 and self.selectedIndex < len(self.data)):
            selected = self.data[self.selectedIndex]
            if (selected is not None):
                self._celldataview.currindex = self.selectedIndex
                if (selected.dataLength() > 0):
                    self._celldataview.reset_entries(selected.data)
                else:
                    self._celldataview.clear_entries()

    def _clearDataView(self):
        self._celldataview.clear_entries()

    # Graph view reference and update methods

    @Property(QObject, notify=vmDataGraphChanged)
    def cellDataGraph(self):
        return self._cellDataGraph

    def _updateGraphView(self):
        if (self.__worker.isFinished() and self.selectedIndex >= 0 and self.selectedIndex < len(self.data)):
            selected = self.data[self.selectedIndex]
            if (selected is not None):
                self._cellDataGraph.clearCellData()
                self._cellDataGraph.addCellData(selected)

    def _clearGraphView(self):
        self._cellDataGraph.clearCellData()

    # Loading files worker

    @Property(bool, notify=workerStateChanged)
    def worker_finished(self) -> bool:
        return self.__worker is None or self.__worker.isFinished()

    @Slot('QVariantList')
    def load_elements(self, url: List[QUrl]) -> None:
        if (self.__worker is None or self.__worker.isFinished()):
            files = []
            for i in range(len(url)):
                files.append(url[i].toLocalFile())
                self._model.addData(OcvSocCellData(files[i]))
            self.__start_worker__(files)

    @Slot(int)
    def reload_single_element_by_index(self, index: int) -> None:
        if (index >= 0 and index < len(self.data)):
            self.reload_single_element(self.data[index])

    @Slot(AbcCellData)
    def reload_single_element(self, obj: AbcCellData) -> None:
        if (self.__worker is None or self.__worker.isFinished()):
            if (obj is not None):
                self.__start_worker__([obj.fileinfo.filepath])

    def __start_worker__(self, filepaths: List[str]):
        self.__worker = LoadXlsFileWorker(filepaths)
        self.__worker.entry_startReading.connect(self.__workerStartReadingFile)
        self.__worker.entry_finishedReading.connect(self.__workerFinishedFile)
        self.__worker.entry_faultedReading.connect(self.__workerFaultedReading)
        self.__worker.start(QThread.LowestPriority)
        self.workerStateChanged.emit()
        self._clearDataView()
        self._clearGraphView()
    
    @Slot(str)
    def __workerStartReadingFile(self, filepath: str):
        self._model.getData(filepath).state = ProcessState.Processing
    
    @Slot(str, 'QVariantList')
    def __workerFinishedFile(self, filepath: str, data: List[List[float]]):
        dataObj = self._model.getData(filepath)
        if dataObj is not None:
            try:
                # clear data before adding new elements
                dataObj.clearData()
                # data[0][0] is the highest capacity of the data
                for valuePair in data:
                    dataObj.add_values(valuePair[1], valuePair[0])

                dataObj.clear_exception()
                dataObj.state = ProcessState.Finished

                self.workerStateChanged.emit()
                self._updateDataView()
                self._updateGraphView()
            except Exception as e:
                dataObj.processException = e

    @Slot(str, Exception)
    def __workerFaultedReading(self, filepath: str, e: Exception):
        dataObj = self._model.getData(filepath)
        dataObj.processException = e
        self.workerStateChanged.emit()