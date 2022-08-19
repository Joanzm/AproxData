from typing import List
from PySide6.QtCore import QThread, Signal, Property, Slot, QUrl, QObject

from ..Abstract.Model.abc_model import AbcCellData
from ..Abstract.Model.abc_celldata import ProcessState
from .Model.ocv_soc_model import OcvSocModel, OcvSocCellData
from ..OcvSoc import ocv_soc_celldataparser_xlr as Parser

class OcvSocLoadXlsFileRunner(QObject):

    workerStateChanged = Signal()

    def __init__(self, model: OcvSocModel) -> None:
        super().__init__()
        self.__worker = None
        self._model = model

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
        self.__worker = OcvSocLoadXlsFileWorker(filePaths)
        self.__worker.entryStartReading.connect(self.__workerStartReadingFile)
        self.__worker.entryFinishedReading.connect(self.__workerFinishedFile)
        self.__worker.entryFaultedReading.connect(self.__workerFaultedReading)
        self.__worker.start(QThread.LowestPriority)
        self.workerStateChanged.emit()
        self._model.clearSignal.emit()
    
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

                if self._model.allDataLoaded():
                    self._model.updateTableSignal.emit()
                    self._model.updateGraphSignal.emit()
            except Exception as e:
                dataObj.processException = e

    @Slot(str, Exception)
    def __workerFaultedReading(self, filePath: str, e: Exception):
        dataObj = self._model.getData(filePath)
        dataObj.processException = e
        self.workerStateChanged.emit()

class OcvSocLoadXlsFileWorker(QThread):

    entryStartReading = Signal(str)
    entryFinishedReading = Signal(str, 'QVariantList')
    entryFaultedReading = Signal(str, Exception)

    def __init__(self, filepaths: List[str]) -> None:
        super().__init__()
        self.__filepaths = filepaths

    def run(self) -> None:
        for f in self.__filepaths:
            try:
                self.entryStartReading.emit(f)
                self.entryFinishedReading.emit(f, Parser.load_sheets(f))
            except Exception as e:
                self.entryFaultedReading.emit(f, e)