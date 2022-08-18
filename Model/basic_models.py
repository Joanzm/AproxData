import os
import time
from typing import List
from PySide6.QtCore import Qt, Property, Signal, QUrl, Slot, QThread, QAbstractListModel, QModelIndex, QObject

class FileInfo(QObject):

    filepath_changed = Signal(str)
    properties_changed = Signal()

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self.__filepath = filepath

    @Property(str, notify=filepath_changed)
    def filepath(self) -> str:
        return self.__filepath

    @filepath.setter
    def filepath(self, value: str) -> None:
        self.__filepath = value
        self.filepath_changed.emit(value)
        self.properties_changed.emit()

    @Property(str, notify=properties_changed)
    def filename(self) -> str:
        return os.path.basename(self.__filepath)

    @Property(float, notify=properties_changed)
    def fileSize(self) -> float:
        return os.path.getsize(self.__filepath) / 1000 # in KB
    
    @Property(str, notify=properties_changed)
    def createDate(self) -> str:
        seconds = os.path.getctime(self.__filepath)
        return time.ctime(seconds)

    @Property(str, notify=properties_changed)
    def lastEditDate(self) -> str:
        seconds = os.path.getmtime(self.__filepath)
        return time.ctime(seconds)

    @Property(str, notify=properties_changed)
    def strDisplay(self) -> str:
        return "Filepath: {}\nFilesize: {} KB\nCreate date: {}\nLast edit date: {}".format(
            self.filepath, self.fileSize, self.createDate, self.lastEditDate)