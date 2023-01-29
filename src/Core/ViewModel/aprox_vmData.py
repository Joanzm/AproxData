from PySide6.QtCore import Qt, QModelIndex, QPersistentModelIndex, QUrl, QThread, QAbstractListModel, Property, Signal, QObject, Slot
from typing import Union, List

from ..Model.aprox_data import DataSet, DataSetReader, ProcessState
from ..Model.aprox_parser import ADataSetParser, CellDatasetParser

from ..Base.fileInfo import FileInfo
from .abc_vmBase import AbcVmBaseViewAll, AbcVmTable, AbcVmGraphViewAll

class QDataSetReader(QObject, DataSetReader):

    stateChanged = Signal()
    processExcepionChanged = Signal()

    def __init__(self, key: str, dataSet: DataSet, parser: ADataSetParser) -> None:
        QObject.__init__(self)
        DataSetReader.__init__(self, key, dataSet, parser)

    @Property(ProcessState, notify=stateChanged)
    def state(self) -> ProcessState:
        return self._state

    @state.setter
    def state(self, value: ProcessState):
        self._state = value
        self.stateChanged.emit()

    def _onChange(self):
        super()._onChange()
        self.stateChanged.emit()
        self.processExcepionChanged.emit()

    @Property(str, notify=stateChanged)
    def stateStr(self) -> str:
        return self._state.name

    @Property(int, notify=stateChanged)
    def stateInt(self) -> int:
        return int(self._state)

    @Property(str, notify=processExcepionChanged)
    def exceptionMessage(self) -> str:
        if (self._error is None):
            return ""
        else:
            return str(self._error)


class QFileDataSetReader(QDataSetReader):

    fileinfoChanged = Signal()

    def __init__(self, filePath: str, dataSet: DataSet, parser: ADataSetParser) -> None:
        super().__init__(filePath, dataSet, parser)
        self._fileInfo = FileInfo(filePath)

    @Property(FileInfo, notify=fileinfoChanged)
    def fileInfo(self) -> FileInfo:
        return self._fileInfo

class QDataSetReaderWorker(QThread):

    started = Signal()
    finished = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.__readers = []

    def setReaders(self, readers: List[DataSetReader]):
        self.__readers = readers

    def run(self) -> None:
        try:
            self.started.emit()
            for r in self.__readers: r.read()
        finally:
            self.finished.emit()

class QDatasetList(QAbstractListModel):

    workerSignal = Signal()
    dataChangedSignal = Signal(object, int)
    selectionChangedSignal = Signal(object, int)
    clearViewSignal = Signal()

    def __init__(self, list: List[QFileDataSetReader] = {}) -> None:
        super().__init__()
        self._selectedIndex = -1
        self._list = list
        self._worker = QDataSetReaderWorker()
        self._datasets = []
        self._worker.started.connect(self.onWorkerStarted)
        self._worker.finished.connect(self.onWorkerFinished)

    @Property(int, notify=selectionChangedSignal)
    def selectedIndex(self) -> int:
        return self._selectedIndex
    
    @selectedIndex.setter
    def selectedIndex(self, value: int):
        if self._selectedIndex is not value and self._worker.isFinished():
            self._selectedIndex = value
            x = [r.dataset for r in self._list]
            self.selectionChangedSignal.emit(x, self._selectedIndex)
    
    # Loading new files

    @Property(bool, notify=workerSignal)
    def workerRunning(self):
        return self._worker.isRunning()

    @Property(bool, notify=workerSignal)
    def workerFinished(self):
        return self._worker.isFinished()

    @Slot()
    def onWorkerStarted(self):
        self.workerSignal.emit()

    @Slot()
    def onWorkerFinished(self):
        self.dataChanged()
        self.workerSignal.emit()

    @Slot('QVariantList')
    def loadElements(self, url: List[QUrl]) -> None:
        if not self._worker.isRunning():
            for i in range(len(url)):
                file = url[i].toLocalFile()
                if (file not in self._list):
                    self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
                    self._list.append(QFileDataSetReader(file, DataSet(file), CellDatasetParser()))
                    self.endInsertRows()
            self.clearViewSignal.emit()
            self._worker.setReaders(self._list)
            self._worker.start(QThread.HighPriority)

    @Slot(int)
    def reloadSingleElementByIndex(self, index: int) -> None:
        self._worker.setReaders([self._list[index]])
        self._worker.start(QThread.HighPriority)

    # Model properties and functions

    cellDataRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            QDatasetList.cellDataRole: b'celldata',
        }

    @Property(bool, notify=dataChangedSignal)
    def hasData(self) -> bool:
        return len(self._list) > 0

    def rowCount(self, parent=QModelIndex()):
       return len(self._list)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == QDatasetList.cellDataRole:
                return self._list[index.row()]
        return None

    @Slot(int)
    def removeData(self, index: int):
        self.beginRemoveRows(QModelIndex(), index, index)
        del self._list[index]
        self.endRemoveRows()
        self.dataChanged()

    @Slot()
    def clearData(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._dataObjects) - 1)
        self._list.clear()
        self.endRemoveRows()
        self.dataChanged()

    @Slot()
    def dataChanged(self):
        self.dataChangedSignal.emit([r.dataset for r in self._list], self._selectedIndex)

class QDataTable(AbcVmBaseViewAll, AbcVmTable):

    def __init__(self) -> None:
        super().__init__()
        self._isHeaderVisible = True
        self._headers = ["Soc", "Voltage"]

    # PUBLIC METHODS
    # Update View

    def onViewAllChanging(self):
        self.viewAllChanged.emit(self._viewAll)

    @Slot()
    def onDataChanged(self, dataObjects: List[DataSet], selectedIndex: int):
        if self._viewAll:
            self.__updateAll(dataObjects)
        else:
            self.__updateSelected(dataObjects, selectedIndex)

    @Slot()
    def onSelectionChanged(self, dataObjects: List[DataSet], selectedIndex: int):
        if not self._viewAll:
            self.__updateSelected(dataObjects, selectedIndex)

    @Slot()
    def onClearView(self):
        self.clearEntries()

    #QAbstractTableModel implementation

    displayRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            QDataTable.displayRole: b'display'
        }

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        if len(self._data) > 0:
            if self._viewAll:
                return len(self._data[0])
            else:
                return 2
        else:
            return 0

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == QDataTable.displayRole:
                if self._viewAll:
                    return self._data[index.row()][index.column()]
                else:
                    if (index.column() == 0):
                        return self._data[index.row()].y
                    elif (index.column() == 1):
                        return self._data[index.row()].x
        return None

    @Slot(QObject)
    def addEntries(self, dataset: DataSet):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(dataset) - 1))
        for i in range(len(dataset)):
            self._data.append(dataset[i])
        self.endInsertRows()
        self.dataChanged.emit(self._data)

    @Slot(int, result="QVariant")
    def getColumnHeaderData(self, section: int):
        return self._headers[section]
    
    # PRIVATE/PROTECTED METHODS
    # Manipulate data

    def __updateAll(self, dataObjects: List[DataSet]):
        self.clearEntries()
        entries = self._listAllData(dataObjects)
        self._headers = entries.pop(0)
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, len(self._headers) - 1)
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(entries) - 1))
        self._data = entries
        self.endInsertRows()
        self.dataChanged.emit(self._data)

    def __updateSelected(self, datasets: List[DataSet], selectedIndex: int,):
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, 1)
        if (selectedIndex >= 0 and selectedIndex < len(datasets)):
            if (datasets[selectedIndex] is not None):
                self.clearEntries()
                self._headers = ["Soc", "Voltage"]
                self.addEntries(datasets[selectedIndex])
    
    def _listAllData(self, datasets: List[DataSet]) -> List:
        """
        Returns a list of all values in self.dataObjects.
        The first entry is a list of header strings.
        Every following entry (index i) is a list
        of float values which are build as follows (n is length of array):
        - [0] = Average x - Value of all self.dataObjects with index i (SOC)
        - [1] ... [n-2] = y - Values of all self.dataObjects with index i (Voltage)
        - [n-1] = Average and max difference y - Value of all self.dataObjects with index i (Voltage)"""
        allData = []

        #Calculate headers and max row length
        headers = ["Avg SOC"]
        maxLength = 0
        for i in range(len(datasets)):
            l = len(datasets[i])
            if (l > maxLength):
                maxLength = l
            headers.append(datasets[i].key)
        headers.append("Diff/Avg Voltage")
        allData.append(headers)
        
        if len(datasets) > 0:
            for i in range(maxLength):
                floatEntries = []
                entry = []
                count = 0
                avgSoc = 0
                for j in range(len(datasets)):
                    if len(datasets[j]) > i:
                        count = count + 1
                        avgSoc = avgSoc + datasets[j][i].y
                        floatEntries.append(datasets[j][i].x)
                        entry.append("{:.4f} V".format(datasets[j][i].x))
                    else:
                        entry.append(None)
                if count > 0:
                    #calculate average voltage
                    avgVoltage = sum(floatEntries) / len(floatEntries)
                    diffVoltage = max(floatEntries) - min(floatEntries)
                    entry.append("{:.4f} V / {:.4f} V".format(diffVoltage, avgVoltage))
                    #calculate average soc and set as first entry
                    entry.insert(0, "{:.4f} %".format(avgSoc / count))
                    allData.append(entry)
        return allData

class QDataGraph(AbcVmGraphViewAll):

    seriesAdded = Signal(str, 'QVariantList')
    seriesRemoved = Signal(str, 'QVariantList')

    def __init__(self) -> None:
        super().__init__()

    def _addData(self, data: DataSet):
        self.seriesAdded.emit(data.key, data)

    def _removeData(self, data: DataSet):
        self.seriesRemoved.emit(data.key, data)

    