import os
import time
from PySide6.QtCore import Property, Signal, QObject

class FileInfo(QObject):

    filePathChanged = Signal(str)
    propertiesChanged = Signal()

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self._filePath = filepath

    @Property(str, notify=filePathChanged)
    def filePath(self) -> str:
        return self._filePath

    @filePath.setter
    def filePath(self, value: str) -> None:
        self._filePath = value
        self.filePathChanged.emit(value)
        self.propertiesChanged.emit()

    @Property(str, notify=propertiesChanged)
    def fileName(self) -> str:
        return os.path.basename(self._filePath)

    @Property(float, notify=propertiesChanged)
    def fileSize(self) -> float:
        return os.path.getsize(self._filePath) / 1000 # in KB

    @Property(str, notify=propertiesChanged)
    def createDate(self) -> str:
        seconds = os.path.getctime(self._filePath)
        return time.ctime(seconds)

    @Property(str, notify=propertiesChanged)
    def lastEditDate(self) -> str:
        seconds = os.path.getmtime(self._filePath)
        return time.ctime(seconds)

    @Property(str, notify=propertiesChanged)
    def strDisplay(self) -> str:
        return "Filepath: {}\nFilesize: {} KB\nCreate date: {}\nLast edit date: {}".format(
            self.filePath, self.fileSize, self.createDate, self.lastEditDate)