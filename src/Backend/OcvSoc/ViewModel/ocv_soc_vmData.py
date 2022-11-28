from typing import List
from PySide6.QtCore import QModelIndex, Slot

from Backend.Abstract.ViewModel.abc_vmData import AbcDataViewModel, AbcCellData
from Backend.OcvSoc.Model.ocv_soc_cellData import OcvSocCellData

class OcvSocDataViewModel(AbcDataViewModel[OcvSocCellData]):
    
    def __init__(self, data: List[OcvSocCellData]) -> None:
        super().__init__(data)
    
    def getData(self, filepath: str) -> OcvSocCellData:
        for i in range(len(self._dataObjects)):
            if (self._dataObjects[i].fileInfo.filePath == filepath):
                return self._dataObjects[i]
        return None

    def listAllData(self) -> List:
        """
        Returns a list of all values in self.dataObjects.
        The first entry is a list of header strings.
        Every following entry (index i) is a list
        of float values which are build as follows (n is length of array):
        - [0] = Average x - Value of all self.dataObjects with index i (SOC)
        - [1] ... [n-2] = y - Values of all self.dataObjects with index i (Voltage)
        - [n-1] = Average y - Value of all self.dataObjects with index i (Voltage)"""
        allData = []

        #Calculate headers and max row length
        headers = ["Avg SOC"]
        maxLength = 0
        for i in range(len(self.dataObjects)):
            l = len(self.dataObjects[i].data)
            if (l > maxLength):
                maxLength = l
            headers.append(self.dataObjects[i].fileInfo.fileName)
        headers.append("Diff/Avg Voltage")
        allData.append(headers)
        
        if len(self.dataObjects) > 0:
            for i in range(maxLength):
                floatEntries = []
                entry = []
                count = 0
                avgSoc = 0
                for j in range(len(self.dataObjects)):
                    if len(self.dataObjects[j].data) > i:
                        count = count + 1
                        avgSoc = avgSoc + self.dataObjects[j].data[i].soc
                        floatEntries.append(self.dataObjects[j].data[i].voltage)
                        entry.append("{:.4f} V".format(self.dataObjects[j].data[i].voltage))
                    else:
                        entry.append(None)
                if count > 0:
                    #calculate average voltage
                    avgVoltage = sum(floatEntries) / len(floatEntries)
                    diffVoltage = max(floatEntries) - min(floatEntries)
                    entry.append("{:.4f} V / {:.4f} V".format(diffVoltage, avgVoltage))
                    #calculate average soc and set as first entry
                    entry.insert(0, "{:.4f} %".format(avgSoc / count))
                    allData.append(entry)
        return allData
