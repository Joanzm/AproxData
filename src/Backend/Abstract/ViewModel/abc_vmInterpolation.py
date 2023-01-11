from PySide6.QtCore import Qt, QObject, Signal, QModelIndex, QPersistentModelIndex, Property, Slot
from abc import abstractmethod
from typing import List, Union

from Backend.Abstract.Model.abc_data import AbcData
from Backend.Abstract.Model.abc_interpolation import IInterpolation
from Backend.Abstract.ViewModel.abc_vmBase import AbcVmTable

class AbcVmInterpolation(AbcVmTable):

    selectedRowChanged = Signal(int)
    lookUpTableChanged = Signal(str)
    graphChanged = Signal(int, 'QVariantList', 'QVariantList')

    lowerLookUpTableSizeChanged = Signal(int)
    upperLookUpTableSizeChanged = Signal(int)

    def __init__(self, interpolation : IInterpolation) -> None:
        super().__init__()
        self._interpolation = interpolation
        self._selectedRow = 0
        self._lowerLookUpTableSize = 2
        self._upperLookUpTableSize = 20
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
        if (value != -1):
            self.lookUpTable = self._interpolation.str_getAlgorithmResultData(self._data[value])
        else:
            self.lookUpTable = ""
        self.graphChanged.emit(value, 
            self._interpolation.list_getAverageData(), 
            self._interpolation.list_getInterpolationPoints(self._data[value]))
        self.selectedRowChanged.emit(value)

    @Property(int, notify=lowerLookUpTableSizeChanged)
    def lowerLookUpTableSize(self) -> int:
        return self._lowerLookUpTableSize
    
    @lowerLookUpTableSize.setter
    def lowerLookUpTableSize(self, value: int):
        self._lowerLookUpTableSize = value
        self.lowerLookUpTableSizeChanged.emit(value)

    @Property(int, notify=upperLookUpTableSizeChanged)
    def upperLookUpTableSize(self) -> int:
        return self._upperLookUpTableSize
    
    @upperLookUpTableSize.setter
    def upperLookUpTableSize(self, value: int):
        self._upperLookUpTableSize = value
        self.upperLookUpTableSizeChanged.emit(value)

    @Property(str, notify=lookUpTableChanged)
    def lookUpTable(self) -> str:
        return self._lookUpTable
    
    @lookUpTable.setter
    def lookUpTable(self, value: str):
        self._lookUpTable = value
        self.lookUpTableChanged.emit(value)

    @Slot()
    def interpolate(self):
        itp = self._interpolation.calculate(self._currDataObjects, 
            self._lowerLookUpTableSize, 
            self._upperLookUpTableSize)
        self.__update(itp)

    # Update View
    # QAbstractTableModel implementation

    @Slot()
    def onDataChanged(self, dataObjects: List[AbcData], selectedIndex: int):
        self._currDataObjects = dataObjects

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
