from typing import List
from PySide6.QtCore import Property, Signal, QObject

from .ViewModel.abc_vmBase import AbcVmBaseChanges
from .ViewModel.aprox_vmData import QDatasetList, QDataTable, QDataGraph
from .ViewModel.aprox_vmInterpolation import AbcVmInterpolation, Vm2DInterpolation

class CellDataAnalyzerViewModel(QObject):

    titleChanged = Signal(str)

    vmChanged = Signal(QObject)
    vmDataTableChanged = Signal(QObject)
    vmDataGraphChanged = Signal(QObject)
    vmInterpolationChanged = Signal(QObject)
    loadFileRunnerChanged = Signal(QObject)

    def __init__(self) -> None:
        super().__init__()
        self._title = ""
        self._cellDataList = QDatasetList([])
        self._cellDataTable = QDataTable()
        self.connectVmBaseSignals(self._cellDataTable)
        self._cellDataGraph = QDataGraph()
        self.connectVmBaseSignals(self._cellDataGraph)
        self._interpolation = Vm2DInterpolation()
        self.connectVmBaseSignals(self._interpolation)
    
    # Title of this model class

    @Property(str, notify=titleChanged)
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value
        self.titleChanged.emit(value)

    # Cell data model

    @Property(QObject, notify=vmChanged)
    def cellDataList(self):
        return self._cellDataList

    # Table view reference and update mehtods

    @Property(QObject, notify=vmDataTableChanged)
    def cellDataTable(self):
        return self._cellDataTable

    # Graph view reference and update methods

    @Property(QObject, notify=vmDataGraphChanged)
    def cellDataGraph(self):
        return self._cellDataGraph

    # Interpolation

    @Property(QObject, notify=vmInterpolationChanged)
    def interpolation(self):
        return self._interpolation

    # Connector methods
    
    def connectVmBaseSignals(self, vm: AbcVmBaseChanges):
        if self._cellDataList and vm:
            self._cellDataList.dataChangedSignal.connect(vm.onDataChanged)
            self._cellDataList.selectionChangedSignal.connect(vm.onSelectionChanged)
            self._cellDataList.clearViewSignal.connect(vm.onClearView)

    