from numpy import ndarray
from typing import List
from abc import ABCMeta, abstractmethod
from Backend.Abstract.Model.abc_data import AbcData

class IInterpolation(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'headers') and 
                callable(subclass.headers) and 
                hasattr(subclass, 'calculate') and 
                callable(subclass.calculate) or 
                hasattr(subclass, 'getAverageDeviation') and 
                callable(subclass.getAverageDeviation) or 
                hasattr(subclass, 'getMinDeviation') and 
                callable(subclass.getMinDeviation) or 
                hasattr(subclass, 'getMaxDeviation') and 
                callable(subclass.getMaxDeviation) or 
                hasattr(subclass, 'getAverageData') and 
                callable(subclass.getAverageData) or 
                hasattr(subclass, 'list_getAverageData') and 
                callable(subclass.list_getAverageData) or 
                hasattr(subclass, 'getLookUpTable') and 
                callable(subclass.getLookUpTable) or 
                hasattr(subclass, 'str_getLookUpTable') and 
                callable(subclass.str_getLookUpTable) or 
                hasattr(subclass, 'getInterpolationPoints') and 
                callable(subclass.getInterpolationPoints) or 
                hasattr(subclass, 'list_getInterpolationPoints') and 
                callable(subclass.list_getInterpolationPoints) or 
                NotImplemented)

    @abstractmethod
    def headers(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, 
        dataObjects: List[AbcData], 
        lowerLookUpTableLimit: int, 
        upperLookUpTableLimit: int) -> List:
            raise NotImplementedError

    @abstractmethod
    def getAverageDeviation(self, data: ndarray) -> float:
        raise NotImplementedError

    @abstractmethod
    def getMinDeviation(self, data: ndarray) -> float:
        raise NotImplementedError

    @abstractmethod
    def getMaxDeviation(self, data: ndarray) -> float:
        raise NotImplementedError

    @abstractmethod
    def getAverageData(self, data: ndarray) -> ndarray:
        raise NotImplementedError

    @abstractmethod
    def list_getAverageData(self, data: ndarray) -> List:
        raise NotImplementedError

    @abstractmethod
    def getLookUpTable(self, size: int, data: ndarray) -> ndarray:
        raise NotImplementedError

    @abstractmethod
    def str_getLookUpTable(self, size: int, data: ndarray) -> str:
        raise NotImplementedError

    @abstractmethod
    def getInterpolationPoints(self, size: int, data: ndarray) -> ndarray:
        raise NotImplementedError

    @abstractmethod
    def list_getInterpolationPoints(self, size: int, data: ndarray) -> List:
        raise NotImplementedError