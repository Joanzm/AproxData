from typing import List
from abc import abstractmethod
import xlrd

class ADataSetParser:

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'parse') and 
                callable(subclass.parse) or 
                NotImplemented)
    
    @property
    def name(self):
        return ""

    @abstractmethod
    def parse(self, key: str) -> List[float]:
        pass

class CellDatasetParser(ADataSetParser):

    @property
    def name(self):
        return "Cell data parser"

    def parse(self, key: str) -> List[float]:
        """Reading all the sheets of the self.book instance (loaded by load_book(...)) for
        the idle capacity voltage pairs and adds them to the cellData two dim array. For all
        files the given idle capacities must be the same or an exception will be thrown."""

        #print("Start parsing file " + filename)
        data = []
        book = xlrd.open_workbook(key, on_demand=True)
        reducedCapacity = 0.0 #The current reduced capacity by the cell tester
        pointer = 0 #Current position to fill self.cellData

        #Skip all first rows until the first discharge step takes place
        startIndex = 1
        sh = book.sheet_by_index(1)
        row = sh.row(startIndex)
        while (sh.row(startIndex)[2].value != "CC_DChg"):
            startIndex += 1

        #Process each sheet (except the first one with basic test informations)
        for nSheet in range(1, book.nsheets):
            sh = book.sheet_by_index(nSheet)
            prevRow = sh.row(startIndex-1)
            #Process each row of the sheet
            for rx in range(startIndex,sh.nrows):
                row = sh.row(rx)
                #If the current row is the last rest entry before a discharge or charge entry add the previous entry to the self.cellData
                if (row[2].value == "CCCV_Chg" or row[2].value == "CC_DChg") and prevRow[2].value == "Rest":
                    #print("{:.4f} Ah | {:.4f} V".format(round(reducedCapacity,4), prevRow[5].value))
                    data.append([prevRow[5].value, round(reducedCapacity,4)])
                    pointer += 1
                elif row[2].value == "Rest" and prevRow[2].value == "CC_DChg":
                    reducedCapacity += round(prevRow[7].value,4)
                prevRow = row
            book.unload_sheet(nSheet)
            startIndex = 1 #Skip first row of each sheet

        book.release_resources()
        data.reverse()

        # Convert capacity in mAh to SOC % => first value is highest capacity.
        if (len(data) > 0):
            highestCapacity = data[0][1]
            for i in range(len(data)):
                data[i][1] = round((highestCapacity - data[i][1]) / highestCapacity, 4)
        return data