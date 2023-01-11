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
                hasattr(subclass, 'getAlgorithmResultData') and 
                callable(subclass.getAlgorithmResultData) or 
                hasattr(subclass, 'str_getAlgorithmResultData') and 
                callable(subclass.str_getAlgorithmResultData) or 
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
    def getAverageDeviation(self, id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def getMinDeviation(self, id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def getMaxDeviation(self, id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def getAverageData(self) -> ndarray:
        raise NotImplementedError

    @abstractmethod
    def list_getAverageData(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def getAlgorithmResultData(self, id: int) -> ndarray:
        raise NotImplementedError

    @abstractmethod
    def str_getAlgorithmResultData(self, id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def getInterpolationPoints(self, id: int, xValues: List[int] = []) -> ndarray:
        raise NotImplementedError

    @abstractmethod
    def list_getInterpolationPoints(self, id: int, xValues: List[int] = []) -> List:
        raise NotImplementedError