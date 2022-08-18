from enum import IntEnum
from PySide6.QtCore import Property, Signal, QModelIndex, QPersistentModelIndex, Slot, QEnum, QObject, QAbstractTableModel
from abc import abstractmethod
from typing import List, TypeVar, Generic, Union

from Model.basic_models import FileInfo

T = TypeVar("T")

@QEnum
class ProcessState(IntEnum):
    Pendeling = 0
    Processing = 1
    Finished = 2
    Faulted = 3

class AbcCellData(QObject, Generic[T]):

    stateChanged = Signal()
    processExcepionChanged = Signal()
    fileinfoChanged = Signal()

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self._fileInfo = FileInfo(filepath)
        self._celldata = []
        self._state = ProcessState.Pendeling
        self._processException = None

    @abstractmethod
    def add_entry(self, entry: type[T]):
        pass

    @Property('QVariantList')
    def data(self) -> List[type[T]]:
        return self._celldata

    def delete_entry(self, row: int):
        del self._celldata[row]

    def clearData(self):
        self._celldata.clear()

    def data_length(self) -> int:
        return len(self._celldata)

    @Property(FileInfo, notify=fileinfoChanged)
    def fileinfo(self) -> FileInfo:
        return self._fileInfo
    
    def set_file(self, value: str):
        self._fileInfo.filepath = value

    @Property(ProcessState, notify=stateChanged)
    def state(self) -> ProcessState:
        return self._state

    @state.setter
    def state(self, value: ProcessState):
        self._state = value
        self.stateChanged.emit()

    @Property(str, notify=stateChanged)
    def state_str(self) -> str:
        return self._state.name

    @Property(int, notify=stateChanged)
    def state_int(self) -> int:
        return int(self._state)

    @Property(Exception, notify=processExcepionChanged)
    def processExcepion(self) -> Exception:
        return self._processException

    @processExcepion.setter
    def processException(self, value: Exception):
        self._processException = value
        if (value is not None):
            self.state = ProcessState.Faulted
        self.processExcepionChanged.emit()

    def clear_exception(self):
        self._processException = None
        self.processExcepionChanged.emit()

    @Property(str, notify=processExcepionChanged)
    def exceptionMessage(self) -> str:
        if (self._processException is None):
            return ""
        else:
            return str(self._processException)
