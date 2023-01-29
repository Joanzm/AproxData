from PySide6.QtCore import Qt, QObject, Signal, QModelIndex, QPersistentModelIndex, Property, Slot
from abc import abstractmethod
from typing import List, Union

from ..Model.aprox_data import DataSet
from ..Model.aprox_interpolation import IInterpolation, LinearInterpolation, PolyfitInterpolation
from .abc_vmBase import AbcVmBaseChanges, AbcVmTable

class AbcVmInterpolation(AbcVmTable, AbcVmBaseChanges):

    selectedRowChanged = Signal(int)
    lookUpTableChanged = Signal(str)
    graphChanged = Signal(int, 'QVariantList', 'QVariantList')

    lowerInteropSizeChanged = Signal(int)
    upperInteropSizeChanged = Signal(int)

    def __init__(self, interpolation : IInterpolation) -> None:
        super().__init__()
        self._interpolation = interpolation
        self._selectedRow = 0
        self._lowerInteropSize = self._interpolation.defaultLowerInteropSize()
        self._upperInteropSize = self._interpolation.defaultUpperInteropSize()
        self._currDataObjects = []
        self._lookUpTable = ""

    # PUBLIC METHODS
    # Setting properties

    @Property(int, notify=selectedRowChanged)
    def selectedRow(self) -> int:
        return self._selectedRow

    @selectedRow.setter
    def selectedRow(self, value: int):
        self._selectedRow = value
        if (value < 0):
            self.lookUpTable = ""
            self.graphChanged.emit(value, None, None)
        else:
            self.lookUpTable = self._interpolation.str_getAlgorithmResultData(self._data[value])
            self.graphChanged.emit(value, 
                self._interpolation.list_getAverageData(), 
                self._interpolation.list_getInterpolationPoints(self._data[value]))
        self.selectedRowChanged.emit(value)

    @Property(int)
    def minInteropSize(self) -> int:
        return self._interpolation.minInteropSize()

    @Property(int)
    def maxInteropSize(self) -> int:
        return self._interpolation.maxInteropSize()

    @Property(int, notify=lowerInteropSizeChanged)
    def lowerInteropSize(self) -> int:
        return self._lowerInteropSize
    
    @lowerInteropSize.setter
    def lowerInteropSize(self, value: int):
        self._lowerInteropSize = value
        self.lowerInteropSizeChanged.emit(value)

    @Property(int, notify=upperInteropSizeChanged)
    def upperInteropSize(self) -> int:
        return self._upperInteropSize
    
    @upperInteropSize.setter
    def upperInteropSize(self, value: int):
        self._upperInteropSize = value
        self.upperInteropSizeChanged.emit(value)

    @Property(str, notify=lookUpTableChanged)
    def lookUpTable(self) -> str:
        return self._lookUpTable
    
    @lookUpTable.setter
    def lookUpTable(self, value: str):
        self._lookUpTable = value
        self.lookUpTableChanged.emit(value)
        
    @abstractmethod
    def changeAlgorithm(self, value: str):
        pass

    @Slot()
    def interpolate(self):
        if (not self._currDataObjects or len(self._currDataObjects) < 1):
            raise Exception("No data yet loaded.")
        lengths = [len(dataObject) for dataObject in self._currDataObjects]
        if (not all(length == lengths[0] for length in lengths)):
            raise Exception("Read data has different x-value lengths. Algorithm can only handle data with equal length.")
        itp = self._interpolation.calculate(self._currDataObjects, 
            self._lowerInteropSize, 
            self._upperInteropSize)
        self.__update(itp)

    @Slot()
    def onDataChanged(self, dataObjects: List[DataSet], selectedIndex: int):
        self._currDataObjects = dataObjects

    @Slot()
    def onSelectionChanged(self, dataObjects: object, selectedIndex: int):
        pass

    @Slot()
    def onClearView(self):
        self.clearEntries()
        self.selectedRow = -1

    # Update View
    # QAbstractTableModel implementation

    displayRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            AbcVmInterpolation.displayRole: b'display'
        }

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        return len(self._interpolation.headers())

    @Slot(QObject)
    def addEntries(self, obj: object):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(obj.data) - 1))
        self._data.append(obj)
        self.endInsertRows()
        self.dataChanged.emit(self._data)

    @Slot(int, result="QVariant")
    def getColumnHeaderData(self, section: int):
        return self._interpolation.headers()[section]

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == AbcVmInterpolation.displayRole:
                if (index.column() == 0):
                    return self._data[index.row()]
                else:
                    val = None
                    prevVal = None
                    if (index.column() == 1):
                        val = self._interpolation.getAverageDeviation(self._data[index.row()])
                        if index.row() > 0:
                            prevVal = self._interpolation.getAverageDeviation(self._data[index.row() - 1])
                    elif (index.column() == 2):
                        val = self._interpolation.getMaxDeviation(self._data[index.row()])
                        if index.row() > 0:
                            prevVal = self._interpolation.getMaxDeviation(self._data[index.row() - 1])
                    
                    if val is not None:
                        if prevVal is not None:
                            return "{:.3f} % ({:+.3f} %)".format(val * 100, (val - prevVal) * 100)
                        else:
                            return "{:.3f} %".format(val * 100)
        return None
    
    # PRIVATE/PROTECTED METHODS
    # Manipulate data

    def __update(self, data: List):
        self.clearEntries()
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, len(self._interpolation.headers()) - 1)
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(data) - 1))
        self._data = data
        self.endInsertRows()
        self.dataChanged.emit(self._data)

class Vm2DInterpolation(AbcVmInterpolation):

    def __init__(self) -> None:
        super().__init__(LinearInterpolation())

    @Slot(str)
    def changeAlgorithm(self, value: str):
        self.onClearView()
        if value == "Linear Interpolation":
            self._interpolation = LinearInterpolation()
        if value == "Polyfit Interpolation":
            self._interpolation = PolyfitInterpolation()
        
        if (self._lowerInteropSize < self._interpolation.minInteropSize()):
            self._lowerInteropSize = self._interpolation.minInteropSize()
        if (self._upperInteropSize > self._interpolation.maxInteropSize()):
            self._upperInteropSize = self._interpolation.maxInteropSize()
