import xlrd
import glob
import csv
import typing

class XLRCellDataParser:
    """
    Creates a new parser instance for collecting idle cell voltage/capacity pairs 
    from the cell tester data (.xls files) for validating SOC algorithm. (For the format see the example file in the git repository)

    Can load one file after another via load_book(...)
    and proccess them via load_sheets(...). The collected data will be added to the self.cellData two dim array.
    """
    
    def __init__(self):
        self.book = None
        self.cellData = []

    def load_book(self, fileName):
        """Creates a new self.book instance with the given fileName from a .xls file.
        
        Parameters:
        fileName (str): The name of the .xls file to be loaded from the given directory."""
        print("Loading file " + fileName + " ...")
        self.book = xlrd.open_workbook(fileName, on_demand=True)

    def load_sheets(self):
        """Reading all the sheets of the self.book instance (loaded by load_book(...)) for
        the idle capacity voltage pairs and adds them to the cellData two dim array. For all
        files the given idle capacities must be the same or an exception will be thrown."""

        reducedCapacity = 0.0 #The current reduced capacity by the cell tester
        pointer = 0 #Current position to fill self.cellData

        #Skip all first rows until the first discharge step takes place
        startIndex = 1
        sh = self.book.sheet_by_index(1)
        row = sh.row(startIndex)
        while (sh.row(startIndex)[2].value != "CC_DChg"):
            startIndex += 1

        #Process each sheet (except the first one with basic test informations)
        for nSheet in range(1, self.book.nsheets):
            sh = self.book.sheet_by_index(nSheet)
            prevRow = sh.row(startIndex-1)
            #Process each row of the sheet
            for rx in range(startIndex,sh.nrows):
                row = sh.row(rx)
                #If the current row is the last rest entry before a discharge or charge entry add the previous entry to the self.cellData
                if (row[2].value == "CCCV_Chg" or row[2].value == "CC_DChg") and prevRow[2].value == "Rest":
                    print("{:.4f} Ah | {:.4f} V".format(round(reducedCapacity,4), prevRow[5].value))
                    if pointer >= len(self.cellData):
                        #If no entry was created yet add a new one
                        self.cellData.append([round(reducedCapacity,4),prevRow[5].value])
                    else:
                        #If an entry already exist check the capacity values (file and 
                        #self.cellData) and if equal add the file value to the capacity list
                        if self.cellData[pointer][0] == round(reducedCapacity,4):
                            self.cellData[pointer].append(prevRow[5].value)
                        else:
                            print("WARNING: Some the file differs in capacity value.")
                            self.cellData[pointer].append(prevRow[5].value)
                    pointer += 1
                elif row[2].value == "Rest" and prevRow[2].value == "CC_DChg":
                    reducedCapacity += round(prevRow[7].value,4)
                prevRow = row
            self.book.unload_sheet(nSheet)
            startIndex = 1 #Skip first row of each sheet

def get_files() -> list[str]:
    """
    Returns the list of all available cell data files in the current directory.
    """
    return glob.glob("Data/*.xls")



def parse():
    """
    Runs a parsing process with the .xls files in the current directory.
    """

    reader = XLRCellDataParser()
    files = get_files()
    for f in files:
        reader.load_book(f)
        reader.load_sheets()
        reader.book.release_resources()

    #Switch Capacity values from reduced capacity of the cell tester to remaining capacity of the cell
    highestCapacity = reader.cellData[len(reader.cellData)-1][0]
    for valRow in reader.cellData:
        valRow[0] = round(highestCapacity - valRow[0], 4)
    
    #Writes values to the SOCAlgorithm_CellData.csv file.
    print(len(reader.cellData))
    f = open("SOCAlgorithm_CellData.csv", 'w', encoding='UTF8', newline='')
    writer = csv.writer(f, delimiter=',')

    header = ["Capacity"]
    for f in files:
        header.append("Voltage_" + f)
    writer.writerow(header)
    writer.writerows(reader.cellData)
    f.close()