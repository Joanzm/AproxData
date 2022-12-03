from PySide6.QtCore import Qt, QModelIndex, QPersistentModelIndex
from typing import Union, List

from Backend.Abstract.Model.abc_data import AbcData
from Backend.Abstract.ViewModel.abc_vmDataTable import AbcDataTable

class OcvSocCellDataTable(AbcDataTable):

    def __init__(self) -> None:
        super().__init__()

    # QAbstractTableModel implementation

    displayRole = Qt.UserRole + 1

    def roleNames(self):
        return {
            OcvSocCellDataTable.displayRole: b'display'
        }

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int:
        if len(self._data) > 0:
            if self._viewAll:
                return len(self._data[0])
            else:
                return 2
        else:
            return 0

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == OcvSocCellDataTable.displayRole:
                if self._viewAll:
                    return self._data[index.row()][index.column()]
                else:
                    if (index.column() == 0):
                        return self._data[index.row()].soc
                    elif (index.column() == 1):
                        return self._data[index.row()].voltage
        return None

    # List all table data
    
    def _listAllData(self, dataObjects: List[AbcData]) -> List:
        """
        Returns a list of all values in self.dataObjects.
        The first entry is a list of header strings.
        Every following entry (index i) is a list
        of float values which are build as follows (n is length of array):
        - [0] = Average x - Value of all self.dataObjects with index i (SOC)
        - [1] ... [n-2] = y - Values of all self.dataObjects with index i (Voltage)
        - [n-1] = Average and max difference y - Value of all self.dataObjects with index i (Voltage)"""
        allData = []

        #Calculate headers and max row length
        headers = ["Avg SOC"]
        maxLength = 0
        for i in range(len(dataObjects)):
            l = len(dataObjects[i].data)
            if (l > maxLength):
                maxLength = l
            headers.append(dataObjects[i].fileInfo.fileName)
        headers.append("Diff/Avg Voltage")
        allData.append(headers)
        
        if len(dataObjects) > 0:
            for i in range(maxLength):
                floatEntries = []
                entry = []
                count = 0
                avgSoc = 0
                for j in range(len(dataObjects)):
                    if len(dataObjects[j].data) > i:
                        count = count + 1
                        avgSoc = avgSoc + dataObjects[j].data[i].soc
                        floatEntries.append(dataObjects[j].data[i].voltage)
                        entry.append("{:.4f} V".format(dataObjects[j].data[i].voltage))
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
