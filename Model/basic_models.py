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
    def file_size(self) -> float:
        return os.path.getsize(self.__filepath) / 1000 # in KB
    
    @Property(str, notify=properties_changed)
    def create_date(self) -> str:
        seconds = os.path.getctime(self.__filepath)
        return time.ctime(seconds)

    @Property(str, notify=properties_changed)
    def last_edit_date(self) -> str:
        seconds = os.path.getmtime(self.__filepath)
        return time.ctime(seconds)

class FloatPoint:

    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    @Property(float)
    def x(self) -> float:
        return self._x

    @Property(float)
    def y(self) -> float:
        return self._y