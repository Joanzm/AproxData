import numpy as np
from typing import List
from Backend.Abstract.Model.abc_interpolation import IInterpolation
from Backend.OcvSoc.Model.ocv_soc_celldata import OcvSocCellData

def _createNumpyDataMatrix(dataObjects: List[OcvSocCellData]) -> np.ndarray:
    """
    Insert all PySide model data from @dataObjects into a numpy array.
    @dataObjects: The current loaded model data.
    """
    lenEntries = len(dataObjects[0].data)
    lenData = len(dataObjects)

    #Create and fill array with all data
    arr = np.arange(lenEntries * 2 * lenData, dtype=np.float32)
    for i in range(lenEntries):
        for j in range(lenData):
            arr[2 * i * lenData + j] = dataObjects[j].data[i].voltage
            arr[2 * i * lenData + j + lenData] = dataObjects[j].data[i].soc
    return arr.reshape((lenEntries, 2, lenData))

class LinearInterpolation(IInterpolation):

    def __init__(self) -> None:
        super().__init__()
        self._dataMatrix = np.zeros(0)
        self._arrayAverage = np.zeros(0)
        self._headers = ['Size', 'Avg Deviation', 'Max Deviation']
        self._interopValues = dict[int, np.ndarray]()
        self._averageDataMatrices = dict[int, np.ndarray]()

    def headers(self) -> List:
        return self._headers

    def calculate(self, 
        dataObjects: List[OcvSocCellData], 
        lowerLookUpTableLimit: int, 
        upperLookUpTableLimit: int) -> List:
            results = []

            self._dataMatrix = _createNumpyDataMatrix(dataObjects)
            self._arrayAverage = self._dataMatrix.mean(axis=2)
            for i in range(lowerLookUpTableLimit, upperLookUpTableLimit + 1):
                self._calculate2dLinear(i)
                results.append(i)
            return results

    def getAverageDeviation(self, id: int) -> float:
        return np.float32(np.average(np.absolute(self._arrayAverage[:, 1] - self._averageDataMatrices[id][:, 1]), axis=0)).item()

    def getMinDeviation(self, id: int) -> float:
        return np.float32(np.min(np.absolute(self._arrayAverage[:, 1] - self._averageDataMatrices[id][:, 1]), axis=0)).item()

    def getMaxDeviation(self, id: int) -> float:
        return np.float32(np.max(np.absolute(self._arrayAverage[:, 1] - self._averageDataMatrices[id][:, 1]), axis=0)).item()

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
        
        npyValues = np.zeros(len(npxValues))
        # Calculate yValues for all x values lower than the lowest bound of the look up table
        lutValue = self._interopValues[id][0,0]
        lutFactor = self._interopValues[id][0,1]
        lutOffset = self._interopValues[id][0,2]
        cond = (npxValues < lutValue)
        npyValues = npyValues + (lutFactor * npxValues + lutOffset) * cond
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
        npyValues = npyValues + (lutFactor * npxValues + lutOffset) * cond
        
        points = np.arange(2 * len(npxValues), dtype=np.float32).reshape(len(npxValues), 2)
        points[:,0] = npxValues
        points[:,1] = npyValues
        return points

    def list_getInterpolationPoints(self, id: int, xValues: List[int] = []) -> List:
        return self.getInterpolationPoints(id, xValues).tolist()

    def _calculate2dLinear(self, id: int):
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

class PolyfitInterpolation(IInterpolation):

    def __init__(self) -> None:
        super().__init__()
        self._dataMatrix = np.zeros(0)
        self._arrayAverage = np.zeros(0)
        self._headers = ['Degree', 'Avg Deviation', 'Max Deviation']
        self._interopValues = dict[int, np.poly1d]()
        self._averageDataMatrices = dict[int, np.ndarray]()

    def headers(self) -> List:
        return self._headers

    def calculate(self, 
        dataObjects: List[OcvSocCellData], 
        lowerLookUpTableLimit: int, 
        upperLookUpTableLimit: int) -> List:
            results = []
            self._dataMatrix = _createNumpyDataMatrix(dataObjects)
            self._arrayAverage = self._dataMatrix.mean(axis=2)
            for i in range(lowerLookUpTableLimit, upperLookUpTableLimit + 1):
                xValues = self._arrayAverage[:,0]
                yValues = self._arrayAverage[:,1]
                p = np.poly1d(np.polyfit(xValues, yValues, i))
                calcYValues = p(xValues)
                calcData = np.arange(2 * len(xValues), dtype=np.float32).reshape(len(xValues), 2)
                calcData[:,0] = xValues
                calcData[:,1] = calcYValues
                self._averageDataMatrices[i] = calcData
                self._interopValues[i] = p
                results.append(i)
            return results

    def getAverageDeviation(self, id: int) -> float:
        return np.float32(np.average(np.absolute(self._arrayAverage[:, 1] - self._averageDataMatrices[id][:, 1]), axis=0)).item()

    def getMinDeviation(self, id: int) -> float:
        return np.float32(np.min(np.absolute(self._arrayAverage[:, 1] - self._averageDataMatrices[id][:, 1]), axis=0)).item()

    def getMaxDeviation(self, id: int) -> float:
        return np.float32(np.max(np.absolute(self._arrayAverage[:, 1] - self._averageDataMatrices[id][:, 1]), axis=0)).item()

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
        npyValues = self._interopValues[id](npxValues)
        points = np.arange(2 * len(npxValues), dtype=np.float32).reshape(len(npxValues), 2)
        points[:,0] = npxValues
        points[:,1] = npyValues
        return points

    def list_getInterpolationPoints(self, id: int, xValues: List[int] = []) -> List:
        return self.getInterpolationPoints(id, xValues).tolist()

    
            

