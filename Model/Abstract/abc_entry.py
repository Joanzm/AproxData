from PySide6.QtCore import QObject, QPointF, Signal, Property
from abc import abstractmethod

from Model.basic_models import FloatPoint

class AbcEntry(QObject):

    def __init__(self) -> None:
        super().__init__()

    @Property(QPointF)
    @abstractmethod
    def point(self) -> QPointF:
        pass