from PySide6.QtCore import Qt, Signal, QModelIndex, QPersistentModelIndex, Slot, QAbstractTableModel
from abc import abstractmethod
from typing import List, TypeVar, Generic, Union

from .abc_vmBase import AbcVmBaseViewAll
from .abc_vmData import AbcDataViewModel, AbcCellData

T = TypeVar("T", bound=AbcDataViewModel)

class AbcCalcGraph(AbcVmBaseViewAll, Generic[T]):

    def __init__(self, model: T) -> None:
        super().__init__(model)
    
    # View all implementation

    def onViewAllChanging(self):
        pass
    
    # Update slots

    @Slot()
    def onDataChanged(self):
        pass

    @Slot()
    def onSelectionChanged(self):
        pass

    @Slot()
    def clear(self):
        pass