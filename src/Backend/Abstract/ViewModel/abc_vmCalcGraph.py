from PySide6.QtCore import Qt, Signal, QModelIndex, QPersistentModelIndex, Slot, QAbstractTableModel
from abc import abstractmethod
from typing import List, TypeVar, Generic, Union

from .abc_vmBase import AbcVmBaseViewAll
from ..Model.abc_data import AbcData

class AbcCalcGraph(AbcVmBaseViewAll):

    def __init__(self) -> None:
        super().__init__()
    
    # PUBLIC METHODS: Update view

    def onViewAllChanging(self):
        pass

    @Slot()
    def onDataChanged(self, dataObjects: List[AbcData], selectedIndex: int, canUpdate: bool):
        pass

    @Slot()
    def onSelectionChanged(self, dataObjects: List[AbcData], selectedIndex: int, canUpdate: bool):
        pass

    @Slot()
    def onClearView(self):
        pass