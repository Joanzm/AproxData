from PySide6.QtCore import Qt, QObject, Signal, QModelIndex, QPersistentModelIndex, Property, Slot
from abc import abstractmethod
from typing import List, Union

from Backend.OcvSoc.Model.ocv_soc_interpolation import OcvSoc2DLinearInterpolation
from Backend.OcvSoc.Model.ocv_soc_celldata import OcvSocCellData
from Backend.Abstract.ViewModel.abc_vmBase import AbcVmTable

class OcvSocInterpolation(AbcVmTable):

    selectedRowChanged = Signal(int)
    lookUpTableChanged = Signal(str)

    lowerLookUpTableSizeChanged = Signal(int)
    upperLookUpTableSizeChanged = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self._interpolation = OcvSoc2DLinearInterpolation()
        self._selectedRow = 0
        self._lowerLookUpTableSize = 2
        self._upperLookUpTableSize = 20
        self._currDataObjects = []
        self._headers = ['Size', 'Avg Deviation', 'Max Deviation']
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
            self.lookUpTable = self._interpolation.str_getLookUpTable(self._data[value][0], self._data[value][1])
        else:
            self.lookUpTable = ""
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
    def onDataChanged(self, dataObjects: List[OcvSocCellData], selectedIndex: int):
        self._currDataObjects = dataObjects

    displayRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            OcvSocInterpolation.displayRole: b'display'
        }

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        return len(self._headers)

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == OcvSocInterpolation.displayRole:
                if (index.column() == 0):
                    return self._data[index.row()][0]
                else:
                    val = None
                    prevVal = None
                    if (index.column() == 1):
                        val = self._interpolation.getAverageDeviation(self._data[index.row()][1])
                        if index.row() > 0:
                            prevVal = self._interpolation.getAverageDeviation(self._data[index.row() - 1][1])
                    elif (index.column() == 2):
                        val = self._interpolation.getMaxDeviation(self._data[index.row()][1])
                        if index.row() > 0:
                            prevVal = self._interpolation.getMaxDeviation(self._data[index.row() - 1][1])
                    
                    if val is not None:
                        if prevVal is not None:
                            return "{:.3f} % ({:+.3f} %)".format(val * 100, (val - prevVal) * 100)
                        else:
                            return "{:.3f} %".format(val * 100)
        return None

    @Slot(QObject)
    def addEntries(self, obj: object):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(obj.data) - 1))
        self._data.append(obj)
        self.endInsertRows()
        self.dataChanged.emit(self._data)
    
    # PRIVATE/PROTECTED METHODS
    # Manipulate data

    def __update(self, data: List):
        self.clearEntries()
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, len(self._headers) - 1)
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(data) - 1))
        self._data = data
        self.endInsertRows()
        self.dataChanged.emit(self._data)
