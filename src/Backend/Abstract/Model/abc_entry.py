from PySide6.QtCore import QObject, QPointF, Property
from abc import abstractmethod

class AbcEntry(QObject):

    def __init__(self) -> None:
        super().__init__()

    @Property(QPointF)
    @abstractmethod
    def point(self) -> QPointF:
        pass