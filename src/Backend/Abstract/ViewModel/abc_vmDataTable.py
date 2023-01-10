from PySide6.QtCore import Qt, QObject, Signal, QModelIndex, QPersistentModelIndex, Slot, QAbstractTableModel
from abc import abstractmethod
from typing import List, Union

from .abc_vmBase import AbcVmTable, AbcVmBaseViewAll
from ..Model.abc_data import AbcData

class AbcDataTable(AbcVmBaseViewAll, AbcVmTable):

    def __init__(self) -> None:
        super().__init__()
        self._isHeaderVisible = True
        self._headers = ["Soc", "Voltage"]

    # PUBLIC METHODS
    # Update View

    def onViewAllChanging(self):
        self.viewAllChanged.emit(self._viewAll)

    @Slot()
    def onDataChanged(self, dataObjects: List[AbcData], selectedIndex: int):
        if self._viewAll:
            self.__updateAll(dataObjects)
        else:
            self.__updateSelected(dataObjects, selectedIndex)

    @Slot()
    def onSelectionChanged(self, dataObjects: List[AbcData], selectedIndex: int):
        if not self._viewAll:
            self.__updateSelected(dataObjects, selectedIndex)

    @Slot()
    def onClearView(self):
        self.clearEntries()

    #QAbstractTableModel implementation

    @Slot(QObject)
    def addEntries(self, obj: AbcData):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(obj.data) - 1))
        for i in range(len(obj.data)):
            self._data.append(obj.data[i])
        self.endInsertRows()
        self.dataChanged.emit(self._data)
    
    # PRIVATE/PROTECTED METHODS
    # Manipulate data
    
    @abstractmethod
    def _listAllData(self, dataObjects: List[AbcData]) -> List:
        pass

    def __updateAll(self, dataObjects: List[AbcData]):
        self.clearEntries()
        entries = self._listAllData(dataObjects)
        self._headers = entries.pop(0)
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, len(self._headers) - 1)
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + (len(entries) - 1))
        self._data = entries
        self.endInsertRows()
        self.dataChanged.emit(self._data)

    def __updateSelected(self, dataObjects: List[AbcData], selectedIndex: int,):
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, 1)
        if (selectedIndex >= 0 and selectedIndex < len(dataObjects)):
            if (dataObjects[selectedIndex] is not None):
                self.clearEntries()
                self._headers = ["Soc", "Voltage"]
                self.addEntries(dataObjects[selectedIndex])
