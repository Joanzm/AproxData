from typing import List
from PySide6.QtCore import Property, Signal, QUrl, Slot, QThread, QObject

from Model.OcvSoc.ocv_soc_model import OcvSocModel

from .Abstract.abc_celldata import AbcCellData
from .OcvSoc.ocv_soc_celldata import OcvSocCellData
from .Abstract.abc_celldata import ProcessState
from .OcvSoc.ocv_soc_celldatatable import OcvSocCellDataView
from .OcvSoc.ocv_soc_celldatagraph import OcvSocCellDataGraph
from .OcvSoc.ocv_soc_runnable import LoadXlsFileWorker

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
        self._cellDataView = OcvSocCellDataView(-1, [])
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
        self.__updateDataView()
        self.__updateGraphView()

    # Table view reference and update mehtods

    @Property(QObject, notify=vmDataTableChanged)
    def cellDataView(self):
        return self._cellDataView

    def __updateDataView(self):
        if (self.__worker.isFinished() and self.selectedIndex >= 0 and self.selectedIndex < len(self.data)):
            selected = self.data[self.selectedIndex]
            if (selected is not None):
                self._cellDataView.currindex = self.selectedIndex
                if (selected.dataLength() > 0):
                    self._cellDataView.resetEntries(selected.data)
                else:
                    self._cellDataView.clear_entries()

    def __clearDataView(self):
        self._cellDataView.clear_entries()

    # Graph view reference and update methods

    @Property(QObject, notify=vmDataGraphChanged)
    def cellDataGraph(self):
        return self._cellDataGraph

    def __updateGraphView(self):
        if (self.__worker.isFinished() and self.selectedIndex >= 0 and self.selectedIndex < len(self.data)):
            selected = self.data[self.selectedIndex]
            if (selected is not None):
                self._cellDataGraph.clearCellData()
                self._cellDataGraph.addCellData(selected)

    def __clearGraphView(self):
        self._cellDataGraph.clearCellData()

    # Loading files worker

    @Property(bool, notify=workerStateChanged)
    def workerFinished(self) -> bool:
        return self.__worker is None or self.__worker.isFinished()

    @Slot('QVariantList')
    def loadElements(self, url: List[QUrl]) -> None:
        if (self.__worker is None or self.__worker.isFinished()):
            files = []
            for i in range(len(url)):
                files.append(url[i].toLocalFile())
                self._model.addData(OcvSocCellData(files[i]))
            self.__start_worker__(files)

    @Slot(int)
    def reloadSingleElementByIndex(self, index: int) -> None:
        if (index >= 0 and index < len(self.data)):
            self.reloadSingleElement(self.data[index])

    @Slot(AbcCellData)
    def reloadSingleElement(self, obj: AbcCellData) -> None:
        if (self.__worker is None or self.__worker.isFinished()):
            if (obj is not None):
                self.__start_worker__([obj.fileInfo.filePath])

    def __start_worker__(self, filePaths: List[str]):
        self.__worker = LoadXlsFileWorker(filePaths)
        self.__worker.entryStartReading.connect(self.__workerStartReadingFile)
        self.__worker.entryFinishedReading.connect(self.__workerFinishedFile)
        self.__worker.entryFaultedReading.connect(self.__workerFaultedReading)
        self.__worker.start(QThread.LowestPriority)
        self.workerStateChanged.emit()
        self.__clearDataView()
        self.__clearGraphView()
    
    @Slot(str)
    def __workerStartReadingFile(self, filePath: str):
        self._model.getData(filePath).state = ProcessState.Processing
    
    @Slot(str, 'QVariantList')
    def __workerFinishedFile(self, filePath: str, data: List[List[float]]):
        dataObj = self._model.getData(filePath)
        if dataObj is not None:
            try:
                # clear data before adding new elements
                dataObj.clearData()
                # data[0][0] is the highest capacity of the data
                for valuePair in data:
                    dataObj.add_values(valuePair[1], valuePair[0])

                dataObj.clearException()
                dataObj.state = ProcessState.Finished

                self.workerStateChanged.emit()
                self.__updateDataView()
                self.__updateGraphView()
            except Exception as e:
                dataObj.processException = e

    @Slot(str, Exception)
    def __workerFaultedReading(self, filePath: str, e: Exception):
        dataObj = self._model.getData(filePath)
        dataObj.processException = e
        self.workerStateChanged.emit()