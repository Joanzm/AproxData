from PySide6.QtCore import Qt, QObject, QAbstractTableModel, QModelIndex, QModelIndex, QPersistentModelIndex, Slot, Property, Signal
from abc import abstractmethod, ABCMeta
from typing import Union

class AbcVmBaseChanges():

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def onDataChanged(self, dataObjects: object, selectedIndex: int):
        pass

    @abstractmethod
    def onSelectionChanged(self, dataObjects: object, selectedIndex: int):
        pass
    
    @abstractmethod
    def onClearView(self):
        pass

class AbcVmBaseViewAll(AbcVmBaseChanges):

    viewAllChanged = Signal(bool)

    def __init__(self) -> None:
        super().__init__()
        self._viewAll = False

    @Property(bool, notify=viewAllChanged)
    def viewAll(self) -> bool:
        return self._viewAll

    @viewAll.setter
    def viewAll(self, value: bool):
        self._viewAll = value
        self.onViewAllChanging()

    @abstractmethod
    def onViewAllChanging(self):
        pass
    
class AbcVmGraph(AbcVmBaseChanges, QObject):
    
    @abstractmethod
    def _addData(self, data: object):
        pass

    @abstractmethod
    def _removeData(self, data: object):
        pass

class AbcVmGraphViewAll(AbcVmGraph, AbcVmBaseViewAll, QObject):
    # Signals for connection in qml GraphView
    seriesCleared = Signal()

    def __init__(self):
        super().__init__()
    
    # PUBLIC METHODS: Update view
        
    def onViewAllChanging(self):
        self.viewAllChanged.emit(self._viewAll)

    @Slot()
    def onDataChanged(self, dataObjects: object, selectedIndex: int):
        if self._viewAll:
            self.__updateAll(dataObjects)
        else:
            self.__updateSelected(dataObjects, selectedIndex)

    @Slot()
    def onSelectionChanged(self, dataObjects: object, selectedIndex: int):
        if not self._viewAll:
            self.__updateSelected(dataObjects, selectedIndex)

    @Slot()
    def onClearView(self):
        self.seriesCleared.emit()

    # PRIVATE METHODS

    def __updateAll(self, dataObjects: object):
        self.seriesCleared.emit()
        for i in range(len(dataObjects)):
            self._addData(dataObjects[i])

    def __updateSelected(self, dataObjects: object, selectedIndex: int,):
        if (selectedIndex >= 0 and selectedIndex < len(dataObjects)):
            if (dataObjects[selectedIndex] is not None):
                self.seriesCleared.emit()
                self._addData(dataObjects[selectedIndex])

    @abstractmethod
    def _addData(self, data: object):
        pass

    @abstractmethod
    def _removeData(self, data: object):
        pass

class AbcVmTable(QAbstractTableModel):

    dataChanged = Signal('QVariantList')
    headerDataChanged = Signal(Qt.Orientation, int, int)

    def __init__(self) -> None:
        super().__init__()
        self._isHeaderVisible = True
        self._data = []

    # PUBLIC METHODS
    #QAbstractTableModel implementation

    @abstractmethod
    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        pass

    @abstractmethod
    def data(self, index, role):
        pass

    @abstractmethod
    def roleNames(self):
        pass

    @abstractmethod
    def addEntries(self, obj: object):
        pass

    @abstractmethod
    def getColumnHeaderData(self, section: int):
        pass

    def rowCount(self, parent=QModelIndex()):
       return len(self._data)

    @Slot(int)
    def deleteEntry(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
        self.dataChanged.emit(self._data)

    @Slot()
    def clearEntries(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data) - 1)
        self._data.clear()
        self.endRemoveRows()
        self.dataChanged.emit(self._data)