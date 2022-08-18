from typing import List
from PySide6.QtCore import Qt, Property, Signal, QUrl, Slot, QThread, QAbstractListModel, QModelIndex, QObject

from .Abstract.abc_celldata import AbcCellData
from .OcvSoc.ocv_soc_celldata import OcvSocCellData
from .Abstract.abc_celldata import ProcessState
from .OcvSoc.ocv_soc_celldatatable import OcvSocCellDataView
from .OcvSoc.ocv_soc_celldatagraph import OcvSocCellDataGraph
from .OcvSoc import ocv_soc_celldataparser_xlr as Parser

class CellDataAnalyzerModel(QAbstractListModel):

    cellDataRole = Qt.UserRole + 1

    COLUMNS = ('Datensaetze',)
    celldataChanged = Signal('QVariantList')
    cellDataViewChanged = Signal()
    cellDataGraphChanged = Signal()
    titleChanged = Signal(str)
    selectedValueChanged = Signal()
    selectedIndexChanged = Signal(int)
    workerStateChanged = Signal()

    def __init__(self, title: str = "Test", celldata: List[AbcCellData] = []) -> None:
        super().__init__()
        self.__worker = None
        self._title = title
        self._celldata = celldata
        self._selectedIndex = 0
        self._celldataview = OcvSocCellDataView(-1, [])
        self._cellDataGraph = OcvSocCellDataGraph()

    # Title of this model class

    @Property(str, notify=titleChanged)
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value
        self.titleChanged.emit(value)
    
    # QAbstractListModel implementation

    def roleNames(self):
        return {
            CellDataAnalyzerModel.cellDataRole: b'celldata',
        }

    def rowCount(self, parent=QModelIndex()):
       return len(self._celldata)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == CellDataAnalyzerModel.cellDataRole:
                return self._celldata[index.row()]
        return None
    
    # Adding/Removing new AbcCellData objects

    @Property('QVariantList', notify=celldataChanged)
    def celldata(self):
        return self._celldata

    @celldata.setter
    def celldata(self, value: List[AbcCellData]):
        self._celldata = value
        self.celldataChanged.emit(value)

    @Slot(AbcCellData)
    def add_celldata(self, data: AbcCellData):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._celldata.append(data)
        self.endInsertRows()
        self.celldataChanged.emit(self._celldata)
        self.selectedValueChanged.emit()

    @Slot(int)
    def delete_celldata(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._celldata[row]
        self.endRemoveRows()
        self.celldataChanged.emit(self._celldata)

    def get_celldata_object(self, filename: str) -> AbcCellData:
        for cd in self._celldata:
            if cd.fileinfo.filepath == filename:
                return cd
        return None

    # Selection implementation

    @Property(int, notify=selectedIndexChanged)
    def selectedIndex(self) -> int:
        return self._selectedIndex
    
    @selectedIndex.setter
    def selectedIndex(self, value: int):
        if (self._selectedIndex != value):
            self._selectedIndex = value
            self.selectedIndexChanged.emit(value)
            self.selectedValueChanged.emit()
            self._updateDataView()
            self._updateGraphView()

    @Property(QObject, notify=selectedValueChanged)
    def selectedValue(self) -> AbcCellData:
        if (self._selectedIndex < 0 or self._selectedIndex > len(self._celldata) - 1):
            return None
        else:
            return self._celldata[self._selectedIndex]

    # Table view reference and update mehtods

    @Property(QObject, notify=cellDataViewChanged)
    def celldataview(self):
        return self._celldataview

    def _updateDataView(self):
        if (self.__worker.isFinished() and self._selectedIndex >= 0 and self._selectedIndex < len(self._celldata)):
            selected = self._celldata[self._selectedIndex]
            if (selected is not None):
                self._celldataview.currindex = self._selectedIndex
                if (selected.data_length() > 0):
                    self._celldataview.reset_entries(selected.data)
                else:
                    self._celldataview.clear_entries()

    def _clearDataView(self):
        self._celldataview.clear_entries()

    # Grapg view reference and update methods

    @Property(QObject, notify=cellDataGraphChanged)
    def cellDataGraph(self):
        return self._cellDataGraph

    def _updateGraphView(self):
        if (self.__worker.isFinished() and self._selectedIndex >= 0 and self._selectedIndex < len(self._celldata)):
            selected = self._celldata[self._selectedIndex]
            if (selected is not None):
                self._cellDataGraph.clearCellData()
                self._cellDataGraph.addCellData(selected)

    def _clearGraphView(self):
        self._cellDataGraph.clearCellData()

    # Loading files worker

    @Slot('QVariantList')
    def load_elements(self, url: List[QUrl]) -> None:
        if (self.__worker is None or self.__worker.isFinished()):
            files = []
            for i in range(len(url)):
                files.append(url[i].toLocalFile())
                self.add_celldata(OcvSocCellData(files[i]))
            self.__start_worker__(files)

    @Slot(int)
    def reload_single_element_by_index(self, index: int) -> None:
        if (index >= 0 and index < len(self._celldata)):
            self.reload_single_element(self._celldata[index])

    @Slot(AbcCellData)
    def reload_single_element(self, obj: AbcCellData) -> None:
        if (self.__worker is None or self.__worker.isFinished()):
            if (obj is not None):
                self.__start_worker__([obj.fileinfo.filepath])

    def __start_worker__(self, filepaths: List[str]):
        self.__worker = LoadXlsFileWorker(filepaths)
        self.__worker.entry_startReading.connect(self.__worker_startReadingFile)
        self.__worker.entry_finishedReading.connect(self.__worker_finishedFile)
        self.__worker.entry_faultedReading.connect(self.__worker_faultedReading)
        self.__worker.start(QThread.LowestPriority)
        self.workerStateChanged.emit()
        self._clearDataView()
        self._clearGraphView()
    
    @Slot(str)
    def __worker_startReadingFile(self, filepath: str):
        self.get_celldata_object(filepath).state = ProcessState.Processing
    
    @Slot(str, 'QVariantList')
    def __worker_finishedFile(self, filepath: str, data: List[List[float]]):
        dataObj = self.get_celldata_object(filepath)
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
    def __worker_faultedReading(self, filepath: str, e: Exception):
        dataObj = self.get_celldata_object(filepath)
        dataObj.processException = e
        self.workerStateChanged.emit()

    @Property(bool, notify=workerStateChanged)
    def worker_finished(self) -> bool:
        return self.__worker is None or self.__worker.isFinished()

class LoadXlsFileWorker(QThread):

    entry_startReading = Signal(str)
    entry_finishedReading = Signal(str, 'QVariantList')
    entry_faultedReading = Signal(str, Exception)

    def __init__(self, filepaths: List[str]) -> None:
        super().__init__()
        self.__filepaths = filepaths

    def run(self) -> None:
        for f in self.__filepaths:
            try:
                self.entry_startReading.emit(f)
                self.entry_finishedReading.emit(f, Parser.load_sheets(f))
            except Exception as e:
                self.entry_faultedReading.emit(f, e)