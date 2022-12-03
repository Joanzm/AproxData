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
            arr = self.createNumpyArray(dataObjects)
            arrAverage = arr.mean(axis=2)
            print(arrAverage)
            for i in range(lowerLookUpTableLimit, upperLookUpTableLimit):
                arrItpValues = self.__calculateInterpolationValues(arrAverage, i)

    def createNumpyArray(self, dataObjects: List[OcvSocCellData]) -> np.ndarray:
        lenEntries = len(dataObjects[0].data)
        lenData = len(dataObjects)

        #Create and fill array with all data
        arr = np.arange(lenEntries * 2 * lenData, dtype=np.float32)
        for i in range(lenEntries):
            for j in range(lenData):
                arr[2 * i * lenData + j] = dataObjects[j].data[i].voltage
                arr[2 * i * lenData + j + lenData] = dataObjects[j].data[i].soc
        return arr.reshape((lenEntries, 2, lenData))

    def __calculateInterpolationValues(self, arrAverage: ndarray, lookUpTableSize: int) -> ndarray:
        select = np.round(np.linspace(0, arrAverage.shape[0] - 1, lookUpTableSize, dtype=np.int64), 0)
        arrItpValues = np.take(arrAverage, select, axis=0)
        arrItpValues = np.repeat(arrItpValues, 2, axis=0)
        arrItpValues = arrItpValues[1:arrItpValues.shape[0] - 1]
        arrItpValues.resize((int(arrItpValues.shape[0] / 2), 4))
        arrItpValues = np.apply_along_axis(self.__calculateFactorOffset, 1, arrItpValues)
        return arrItpValues

    def __calculateFactorOffset(self, arr: ndarray) -> List:
        factor = (arr[3] - arr[1]) / (arr[2] - arr[0])
        offset = arr[1] - factor * arr[0]
        return np.array([factor, offset], dtype=np.float32)
            

