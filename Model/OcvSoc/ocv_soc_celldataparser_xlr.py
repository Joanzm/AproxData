import xlrd
import glob
import csv
from typing import List

def load_sheets(filename: str) -> List[List[float]]:
    """Reading all the sheets of the self.book instance (loaded by load_book(...)) for
    the idle capacity voltage pairs and adds them to the cellData two dim array. For all
    files the given idle capacities must be the same or an exception will be thrown."""

    #print("Start parsing file " + filename)
    celldata = []
    book = xlrd.open_workbook(filename, on_demand=True)
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
                celldata.append([round(reducedCapacity,4),prevRow[5].value])
                pointer += 1
            elif row[2].value == "Rest" and prevRow[2].value == "CC_DChg":
                reducedCapacity += round(prevRow[7].value,4)
            prevRow = row
        book.unload_sheet(nSheet)
        startIndex = 1 #Skip first row of each sheet

    book.release_resources()
    celldata.reverse()

    if (len(celldata) > 0):
        highestCapacity = celldata[0][0]
        for i in range(len(celldata)):
            celldata[i][0] =  round((highestCapacity - celldata[i][0]) / highestCapacity, 4)

    return celldata

def get_files() -> list[str]:
    """
    Returns the list of all available cell data files in the current directory.
    """
    return glob.glob("Data/*.xls")

def parse():
    """
    Runs a parsing process with the .xls files in the current directory.
    """

    celldatas = []
    files = get_files()
    for f in files:
        celldatas.append(load_sheets(f))

    #Switch Capacity values from reduced capacity of the cell tester to remaining capacity of the cell
    # highestCapacity = reader.cellData[len(reader.cellData)-1][0]
    # for valRow in reader.cellData:
    #     valRow[0] = round(highestCapacity - valRow[0], 4)
    
    #Writes values to the SOCAlgorithm_CellData.csv file.
    # print(len(reader.cellData))
    # f = open("SOCAlgorithm_CellData.csv", 'w', encoding='UTF8', newline='')
    # writer = csv.writer(f, delimiter=',')

    # header = ["Capacity"]
    # for f in files:
    #     header.append("Voltage_" + f)
    # writer.writerow(header)
    # writer.writerows(reader.cellData)
    # f.close()