from typing import List
from PySide6.QtCore import Property, Signal, QObject

from .Abstract.ViewModel.abc_vmBase import AbcVmBaseChanges
from .OcvSoc.ViewModel.ocv_soc_vmDataList import OcvSocDataListViewModel

from .OcvSoc.ViewModel.ocv_soc_vmInterpolation import OcvSocInterpolation
from .OcvSoc.ViewModel.ocv_soc_vmCellDataTable import OcvSocCellDataTable
from .OcvSoc.ViewModel.ocv_soc_vmCellDataGraph import OcvSocCellDataGraph
from .OcvSoc.Model.ocv_soc_fileRunnable import OcvSocFileRunner

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
        self._runner = OcvSocFileRunner()
        self._cellDataList = OcvSocDataListViewModel([])
        self.connectRunnerSignals(self._cellDataList)
        self._cellDataTable = OcvSocCellDataTable()
        self.connectVmBaseSignals(self._cellDataTable)
        self._cellDataGraph = OcvSocCellDataGraph()
        self.connectVmBaseSignals(self._cellDataGraph)
        self._interpolation = OcvSocInterpolation()
        self.connectInterpolationSignals(self._interpolation)

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

    def connectRunnerSignals(self, vm: OcvSocDataListViewModel):
        if self._runner and vm:
            self._runner.runnerStateChanged.connect(vm.onRunnerStateChanged)
            self._runner.entryStartReading.connect(vm.onRunnerStartReadingFile)
            self._runner.entryFinishedReading.connect(vm.onRunnerFinishedFile)
            self._runner.entryFaultedReading.connect(vm.onRunnerFaultedReading)
            vm.startReading.connect(self._runner.startFileRunner)

    def connectInterpolationSignals(self, vm: OcvSocInterpolation):
        if self._cellDataList and vm:
            self._cellDataList.dataChangedSignal.connect(vm.onDataChanged)

    