import numpy as np

from PySide6.QtCore import Property, Signal, Property, Slot, QUrl
from typing import List

from ...Abstract.Model.abc_data import AbcData, ProcessState

from ..Model.ocv_soc_celldata import OcvSocCellData
from ...Abstract.ViewModel.abc_vmDataList import AbcDataList

class OcvSocDataListViewModel(AbcDataList[OcvSocCellData]):
    
    runnerStateChanged = Signal(bool)
    startReading = Signal('QVariantList')

    def __init__(self, data: List[OcvSocCellData]) -> None:
        super().__init__(data)
        self.__runnerFinished = True
    
    # PUBLIC METHODS
    # Implement abstract methods
    
    def getData(self, filepath: str) -> OcvSocCellData:
        for i in range(len(self._dataObjects)):
            if (self._dataObjects[i].fileInfo.filePath == filepath):
                return self._dataObjects[i]
        return None
    
    # Loading new files

    @Slot('QVariantList')
    def loadElements(self, url: List[QUrl]) -> None:
        if self.__runnerFinished:
            files = []
            for i in range(len(url)):
                files.append(url[i].toLocalFile())
                data = self.getData(url[i].toLocalFile())
                if (data is None):
                    self.addData(OcvSocCellData(files[i]))
                else:
                    data.clearData()
                    data.state = ProcessState.Pendeling
            self.startReading.emit(files)
            self.clearView()

    @Slot(int)
    def reloadSingleElementByIndex(self, index: int) -> None:
        if index >= 0 and index < len(self.dataObjects):
            self.reloadSingleElement(self.dataObjects[index])

    @Slot(AbcData)
    def reloadSingleElement(self, obj: AbcData) -> None:
        if obj is not None and self.__runnerFinished:
            self.startReading.emit([obj.fileInfo.filePath])
    
    @Property(bool, notify=runnerStateChanged)
    def runnerFinished(self) -> bool:
        return self.__runnerFinished

    # Connector to OcvSocFileRunner

    @Slot(bool)
    def onRunnerStateChanged(self, value: bool):
        self.__runnerFinished = value
        self.runnerStateChanged.emit(value)
        if value:
            self.dataChanged()

    @Slot(str)
    def onRunnerStartReadingFile(self, filePath: str):
        self.getData(filePath).state = ProcessState.Processing
    
    @Slot(str, 'QVariantList')
    def onRunnerFinishedFile(self, filePath: str, data: List[List[float]]):
        dataObj = self.getData(filePath)
        if dataObj is not None:
            try:
                # clear data before adding new elements
                dataObj.clearData()
                # data[0][0] is the highest capacity of the data
                for valuePair in data:
                    dataObj.add_values(valuePair[1], valuePair[0])

                dataObj.clearException()
                dataObj.state = ProcessState.Finished
            except Exception as e:
                dataObj.processException = e

    @Slot(str, Exception)
    def onRunnerFaultedReading(self, filePath: str, e: Exception):
        dataObj = self.getData(filePath)
        dataObj.processException = e
