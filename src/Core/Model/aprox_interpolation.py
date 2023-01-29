import numpy as np
from typing import List
from abc import ABCMeta, abstractmethod
from .aprox_data import DataSet

class IInterpolation(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'maxInteropSize') and 
                callable(subclass.maxInteropSize) or 
                hasattr(subclass, 'minInteropSize') and 
                callable(subclass.minInteropSize) or 
                hasattr(subclass, 'defaultUpperInteropSize') and 
                callable(subclass.defaultUpperInteropSize) or 
                hasattr(subclass, 'defaultLowerInteropSize') and 
                callable(subclass.defaultLowerInteropSize) or 
                hasattr(subclass, 'headers') and 
                callable(subclass.headers) or 
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
    def maxInteropSize(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def minInteropSize(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def defaultUpperInteropSize(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def defaultLowerInteropSize(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def headers(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, 
        dataObjects: List[DataSet], 
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
    def getAverageData(self) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def list_getAverageData(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def getAlgorithmResultData(self, id: int) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def str_getAlgorithmResultData(self, id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def getInterpolationPoints(self, id: int, xValues: List[int] = []) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def list_getInterpolationPoints(self, id: int, xValues: List[int] = []) -> List:
        raise NotImplementedError

class LinearInterpolation(IInterpolation):

    def __init__(self) -> None:
        super().__init__()
        self._dataMatrix = np.zeros(0)
        self._arrayAverage = np.zeros(0)
        self._headers = ['Points', 'Avg Deviation', 'Max Deviation']
        self._interopValues = dict[int, np.ndarray]()
        self._averageDataMatrices = dict[int, np.ndarray]()
        self._deviations = dict[int, List[float]]()

    def minInteropSize(self) -> int:
        return 2

    def maxInteropSize(self) -> int:
        return 150

    def defaultLowerInteropSize(self) -> int:
        return 2
    
    def defaultUpperInteropSize(self) -> int:
        return 20

    def headers(self) -> List:
        return self._headers

    def calculate(self, 
        dataObjects: List[DataSet], 
        lowerLookUpTableLimit: int, 
        upperLookUpTableLimit: int) -> List:
            if (len(dataObjects[0]) < upperLookUpTableLimit):
                raise Exception("The upper value is bigger than the amount of data x-values. Upper value must be lower than {max}.".format(max = len(dataObjects[0])) + 1)
            results = []
            self._dataMatrix = CreateNumpyDataMatrix(dataObjects)
            self._arrayAverage = self._dataMatrix.mean(axis=2)
            for i in range(lowerLookUpTableLimit, upperLookUpTableLimit + 1):
                self._calculate1dLinear(i)
                self._calculateDeviations(i)
                results.append(i)
            return results

    def getAverageDeviation(self, id: int) -> float:
        return self._deviations[id][0] # 0 => Average

    def getMinDeviation(self, id: int) -> float:
        return self._deviations[id][1] # 1 => Minimum

    def getMaxDeviation(self, id: int) -> float:
        return self._deviations[id][2] # 2 => Maximum

    def getAverageData(self) -> np.ndarray:
        return self._arrayAverage

    def list_getAverageData(self) -> List:
        return self.getAverageData().tolist()

    def getAlgorithmResultData(self, id: int) -> np.ndarray:
        return self._interopValues[id]

    def str_getAlgorithmResultData(self, size: int) -> str:
        return self.getAlgorithmResultData(size).__str__()

    def getInterpolationPoints(self, id: int, xValues: List[int] = []) -> np.ndarray:
        npxValues = np.zeros(0)
        if not xValues or len(xValues) == 0:
            npxValues = self._arrayAverage[:,0]
        else:
            npxValues = np.array(xValues)
        return self._getInterpolationPointsNP(id, npxValues)

    def list_getInterpolationPoints(self, id: int, xValues: List[int] = []) -> List:
        return self.getInterpolationPoints(id, xValues).tolist()      

    def _getInterpolationPointsNP(self, id: int, npxValues: np.ndarray) -> np.ndarray:
        npyValues = self._getYInterpolationValuesNP(id, npxValues)
        points = np.arange(2 * len(npxValues), dtype=np.float32).reshape(len(npxValues), 2)
        points[:,0] = npxValues
        points[:,1] = npyValues
        return points

    def _getYInterpolationValuesNP(self, id: int, npxValues: np.ndarray) -> np.ndarray:
        npyValues = np.zeros(npxValues.shape)

        # Calculate yValues for all x values lower than the lowest bound of the look up table
        lutValue = self._interopValues[id][0,0]
        lutFactor = self._interopValues[id][0,1]
        lutOffset = self._interopValues[id][0,2]
        cond = (npxValues < lutValue)
        npyValues = npyValues + (lutFactor * npxValues + lutOffset) * cond[:,]

        # Calculate all values in between
        for i in range(0, len(self._interopValues[id][:,0])-1):
            lutValue = self._interopValues[id][i,0]
            lutValueNext = self._interopValues[id][i+1,0]
            lutFactor = self._interopValues[id][i,1]
            lutOffset = self._interopValues[id][i,2]
            cond = (npxValues >= lutValue) & (npxValues < lutValueNext)
            npyValues = npyValues + (lutFactor * npxValues + lutOffset) * cond

        # Calculate yValues for all x values greater than the upper bound of the look up table
        lutValue = self._interopValues[id][-1,0]
        lutFactor = self._interopValues[id][-1,1]
        lutOffset = self._interopValues[id][-1,2]
        cond = (npxValues >= lutValue)  

        return npyValues + (lutFactor * npxValues + lutOffset) * cond

    def _calculate1dLinear(self, id: int):
        """
        Calcualtes the linear interpolation (factor and offset values) for a given @lookUpTableSize
        @arrAverage: The average measure data.
        @lookUpTableSize: The size of the look up table to be calcualted from the measure data.
        @returns: An array same size as arrAverage with factor and offset value for each measure data entry.
        """
        # Calculate indices for equidistant sectors in 
        # the measure data to get the look up table for the given lookUpTableSize.
        select = self._getSelectMask(self._arrayAverage.shape[0] - 1, id)

        # Calculate the element counts (size) for each select sector.
        counts = select[1:select.shape[0]] - select[0:select.shape[0] - 1]
        counts[-1] = counts[-1] + 1 #+1 for last element, is needed to fit size the @arrAverage.

        # Take the measure data for each select index and calculate
        # the linear interpolated factor and offset for each sector.
        arrItpValues = np.take(self._arrayAverage, select, axis=0)
        arrItpValues = np.repeat(arrItpValues, 2, axis=0)
        arrItpValues = arrItpValues[1:arrItpValues.shape[0] - 1]
        arrItpValues.resize((int(arrItpValues.shape[0] / 2), 4))
        self._interopValues[id] = np.apply_along_axis(self._calculateFactorOffset, 1, arrItpValues)

        # Calculate average data matrix for the given amount of points
        arrResult = self.getInterpolationPoints(id)
        self._averageDataMatrices[id] = arrResult

    def _calculateFactorOffset(self, arr: np.ndarray) -> List:
        """
        Calculate factor and offset from a two points in the
        measure dat.
        """
        factor = (arr[3] - arr[1]) / (arr[2] - arr[0])
        offset = arr[1] - factor * arr[0]
        return np.array([arr[0], factor, offset], dtype=np.float32)

    def _getSelectMask(self, maxValue: int, count: int) -> np.ndarray:
        # Calculate indices for equidistant sectors in 
        # the measure data to get the look up table for the given lookUpTableSize.
        return np.round(np.linspace(0, maxValue, count, dtype=np.int64), 0)

    def _calculateDeviations(self, id: int):
        """Calculate deviations: [0] Average; [1] Minimum; [2] Maximum"""
        calcYValues = self._getYInterpolationValuesNP(id, self._dataMatrix[:,0])
        currDeviation = [-1.0, -1.0, -1.0]
        currDeviation[0] = np.float32(np.average(np.abs(calcYValues - self._dataMatrix[:, 1]))).item()
        currDeviation[1] = np.float32(np.min(np.abs(calcYValues - self._dataMatrix[:, 1]))).item()
        currDeviation[2] = np.float32(np.max(np.abs(calcYValues - self._dataMatrix[:, 1]))).item()
        self._deviations[id] = currDeviation

class PolyfitInterpolation(IInterpolation):

    def __init__(self) -> None:
        super().__init__()
        self._dataMatrix = np.zeros(0)
        self._arrayAverage = np.zeros(0)
        self._headers = ['Degree', 'Avg Deviation', 'Max Deviation']
        self._interopValues = dict[int, np.poly1d]()
        self._averageDataMatrices = dict[int, np.ndarray]()
        self._deviations = dict[int, List[float]]()

    def minInteropSize(self) -> int:
        return 1

    def maxInteropSize(self) -> int:
        return 20
    
    def defaultLowerInteropSize(self) -> int:
        return 2

    def defaultUpperInteropSize(self) -> int:
        return 15

    def headers(self) -> List:
        return self._headers

    def calculate(self, 
        dataObjects: List[DataSet], 
        lowerLookUpTableLimit: int, 
        upperLookUpTableLimit: int) -> List:
            results = []
            self._dataMatrix = CreateNumpyDataMatrix(dataObjects)
            self._arrayAverage = self._dataMatrix.mean(axis=2)
            for i in range(lowerLookUpTableLimit, upperLookUpTableLimit + 1):
                self._calculateCoefficients(i)
                self._calculateDeviations(i)
                results.append(i)
            return results

    def getAverageDeviation(self, id: int) -> float:
        return self._deviations[id][0] # 0 => Average

    def getMinDeviation(self, id: int) -> float:
        return self._deviations[id][1] # 1 => Minimum

    def getMaxDeviation(self, id: int) -> float:
        return self._deviations[id][2] # 2 => Maximum

    def getAverageData(self) -> np.ndarray:
        return self._arrayAverage

    def list_getAverageData(self) -> List:
        return self._arrayAverage.tolist()

    def getAlgorithmResultData(self, id: int) -> np.ndarray:
        return self._interopValues[id].coef

    def str_getAlgorithmResultData(self, id: int) -> str:
        return self._interopValues[id].coef.__str__()

    def getInterpolationPoints(self, id: int, xValues: List[int] = []) -> np.ndarray:
        npxValues = np.zeros(0)
        if not xValues or len(xValues) == 0:
            npxValues = self._arrayAverage[:,0]
        else:
            npxValues = np.array(xValues)
        return self._getInterpolationPointsNP(id, npxValues)

    def list_getInterpolationPoints(self, id: int, xValues: List[int] = []) -> List:
        return self.getInterpolationPoints(id, xValues).tolist()

    def _getInterpolationPointsNP(self, id: int, npxValues: np.ndarray) -> np.ndarray:
        npyValues = self._getYInterpolationValuesNP(id, npxValues)
        points = np.arange(2 * len(npxValues), dtype=np.float32).reshape(len(npxValues), 2)
        points[:,0] = npxValues
        points[:,1] = npyValues
        return points

    def _getYInterpolationValuesNP(self, id: int, npxValues: np.ndarray) -> np.ndarray:
        return self._interopValues[id](npxValues)

    def _calculateCoefficients(self, id: int):
        xValues = self._arrayAverage[:,0]
        yValues = self._arrayAverage[:,1]
        p = np.poly1d(np.polyfit(xValues, yValues, id))
        calcYValues = p(xValues)
        calcData = np.arange(2 * len(xValues), dtype=np.float32).reshape(len(xValues), 2)
        calcData[:,0] = xValues
        calcData[:,1] = calcYValues
        self._averageDataMatrices[id] = calcData
        self._interopValues[id] = p

    def _calculateDeviations(self, id: int):
        """Calculate deviations: [0] Average; [1] Minimum; [2] Maximum"""
        calcYValues = self._getYInterpolationValuesNP(id, self._dataMatrix[:,0])
        currDeviation = [-1.0, -1.0, -1.0]
        currDeviation[0] = np.float32(np.average(np.abs(calcYValues - self._dataMatrix[:, 1]))).item()
        currDeviation[1] = np.float32(np.min(np.abs(calcYValues - self._dataMatrix[:, 1]))).item()
        currDeviation[2] = np.float32(np.max(np.abs(calcYValues - self._dataMatrix[:, 1]))).item()
        self._deviations[id] = currDeviation

def CreateNumpyDataMatrix(dataObjects: List[DataSet]) -> np.ndarray:
    """
    Insert all PySide model data from @dataObjects into a numpy array.
    @dataObjects: The current loaded model data.
    """
    lenEntries = len(dataObjects[0])
    lenData = len(dataObjects)

    #Create and fill array with all data
    arr = np.arange(lenEntries * 2 * lenData, dtype=np.float32)
    for i in range(lenEntries):
        for j in range(lenData):
            arr[2 * i * lenData + j] = dataObjects[j][i].x
            arr[2 * i * lenData + j + lenData] = dataObjects[j][i].y
    return arr.reshape((lenEntries, 2, lenData))