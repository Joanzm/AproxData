from typing import List
from PySide6.QtCore import QThread, Signal, Slot, QObject

from Backend.OcvSoc.Model.ocv_soc_celldataparser_xlr import XlrParser

class OcvSocFileRunner(QObject):

    runnerStateChanged = Signal(bool)
    entryStartReading = Signal(str)
    entryFinishedReading = Signal(str, 'QVariantList')
    entryFaultedReading = Signal(str, Exception)

    def __init__(self) -> None:
        super().__init__()
        self.__worker = None

    def startFileRunner(self, filePaths: List[str]):
        self.__worker = OcvSocFileWorker(filePaths)
        self.__worker.entryStartReading.connect(self.__runnerStartReadingFile)
        self.__worker.entryFinishedReading.connect(self.__runnerFinishedFile)
        self.__worker.entryFaultedReading.connect(self.__runnerFaultedReading)
        self.__worker.start(QThread.HighPriority)
        self.runnerStateChanged.emit(self.__runnerFinished())

    def __runnerFinished(self) -> bool:
        return self.__worker is None or self.__worker.isFinished()
    
    @Slot(str)
    def __runnerStartReadingFile(self, filePath: str):
        self.entryStartReading.emit(filePath)
    
    @Slot(str, 'QVariantList')
    def __runnerFinishedFile(self, filePath: str, data: List[List[float]]):
        self.entryFinishedReading.emit(filePath, data)
        self.runnerStateChanged.emit(self.__runnerFinished())

    @Slot(str, Exception)
    def __runnerFaultedReading(self, filePath: str, e: Exception):
        self.entryFaultedReading.emit(filePath, e)
        self.runnerStateChanged.emit(self.__runnerFinished())

class OcvSocFileWorker(QThread):

    entryStartReading = Signal(str)
    entryFinishedReading = Signal(str, 'QVariantList')
    entryFaultedReading = Signal(str, Exception)

    def __init__(self, filepaths: List[str]) -> None:
        super().__init__()
        self.__xlrParser = XlrParser()
        self.__filepaths = filepaths

    def run(self) -> None:
        for f in self.__filepaths:
            try:
                self.entryStartReading.emit(f)
                self.entryFinishedReading.emit(f, self.__xlrParser.load_sheets(f))
            except Exception as e:
                self.entryFaultedReading.emit(f, e)