from PySide6.QtCore import Property, Signal
from abc import abstractmethod
from .abc_vmData import AbcDataViewModel

class AbcVmBaseChanges():

    def __init__(self, model: AbcDataViewModel) -> None:
        super().__init__()
        self._model = model
        self._model.dataChangedSignal.connect(self.onDataChanged)
        self._model.selectionChangedSignal.connect(self.onSelectionChanged)
        self._model.clearViewSignal.connect(self.clear)

    @abstractmethod
    def onDataChanged(self):
        pass

    @abstractmethod
    def onSelectionChanged(self):
        pass
    
    @abstractmethod
    def clear(self):
        pass

class AbcVmBaseViewAll(AbcVmBaseChanges):

    viewAllChanged = Signal(bool)

    def __init__(self, model: AbcDataViewModel) -> None:
        super().__init__(model)
        self._viewAll = False

    @Property(bool, notify=viewAllChanged)
    def viewAll(self) -> bool:
        return self._viewAll

    @viewAll.setter
    def viewAll(self, value: bool):
        self._viewAll = value
        self.onViewAllChanging()
        self.onDataChanged()

    @abstractmethod
    def onViewAllChanging(self):
        pass