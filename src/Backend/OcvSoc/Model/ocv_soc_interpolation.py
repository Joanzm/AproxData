import numpy as np
from numpy import ndarray, dtype, float32
from typing import List

from Backend.OcvSoc.Model.ocv_soc_cellData import OcvSocCellData

class OcvSoc2DLinearInterpolation:

    def __init__(self) -> None:
        super().__init__()

    def calculate(self, 
        dataObjects: List[OcvSocCellData], 
        lowerLookUpTableLimit: int, 
        upperLookUpTableLimit: int) -> List:
            results = []
            arr = self._createNumpyArray(dataObjects)
            arrAverage = arr.mean(axis=2)
            for i in range(lowerLookUpTableLimit, upperLookUpTableLimit + 1):
                arrItpValues = self._getInterpolationValues(arrAverage, i)
                arrResult = np.concatenate((arrAverage, arrItpValues), axis=1, dtype=np.float32)
                arrResult = np.apply_along_axis(self._calculateYValue, 1, arrResult)
                results.append([i, arrResult])
            return results

    def getAverageDeviation(self, data: np.ndarray) -> float:
        return np.float32(np.average(np.absolute(data[:, 1] - data[:, -1]), axis=0)).item()

    def getMinDeviation(self, data: np.ndarray) -> float:
        return np.float32(np.min(np.absolute(data[:, 1] - data[:, -1]), axis=0)).item()

    def getMaxDeviation(self, data: np.ndarray) -> float:
        return np.float32(np.max(np.absolute(data[:, 1] - data[:, -1]), axis=0)).item()

    def _createNumpyArray(self, dataObjects: List[OcvSocCellData]) -> np.ndarray:
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

    def _getInterpolationValues(self, arrAverage: ndarray, lookUpTableSize: int) -> ndarray:
        """
        Calcualtes the linear interpolation (factor and offset values) for a given @lookUpTableSize
        @arrAverage: The average measure data.
        @lookUpTableSize: The size of the look up table to be calcualted from the measure data.
        @returns: An array same size as arrAverage with factor and offset value for each measure data entry.
        """
        # Calculate indices for equidistant sectors in 
        # the measure data to get the look up table for the given lookUpTableSize.
        select = np.round(np.linspace(0, arrAverage.shape[0] - 1, lookUpTableSize, dtype=np.int64), 0)

        # Calculate the element counts (size) for each select sector.
        counts = select[1:select.shape[0]] - select[0:select.shape[0] - 1]
        counts[-1] = counts[-1] + 1 #+1 for last element, is needed to fit size the @arrAverage.

        # Take the measure data for each select index and calculate
        # the linear interpolated factor and offset for each sector.
        arrItpValues = np.take(arrAverage, select, axis=0)
        arrItpValues = np.repeat(arrItpValues, 2, axis=0)
        arrItpValues = arrItpValues[1:arrItpValues.shape[0] - 1]
        arrItpValues.resize((int(arrItpValues.shape[0] / 2), 4))
        arrItpValues = np.apply_along_axis(self._calculateInterpolationValues, 1, arrItpValues)
        # Inflate factor and offset values to the given sector size.
        arrItpValues = np.repeat(arrItpValues, counts, axis=0)
        return arrItpValues

    def _calculateInterpolationValues(self, arr: ndarray) -> List:
        """
        Calculate factor and offset from a two points in the
        measure dat.
        """
        factor = (arr[3] - arr[1]) / (arr[2] - arr[0])
        offset = arr[1] - factor * arr[0]
        return np.array([factor, offset], dtype=np.float32)

    def _calculateYValue(self, arr: ndarray) -> List:
        """
        Calculates the y-Value for a given row containing
        measure data and interpolation values
        """
        yValue = arr[2] * arr[0] + arr[3]
        return np.append(arr, yValue)
            

