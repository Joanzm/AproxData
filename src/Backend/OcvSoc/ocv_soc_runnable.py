from typing import List
from PySide6.QtCore import QThread, Signal

from ..OcvSoc import ocv_soc_celldataparser_xlr as Parser

class LoadXlsFileWorker(QThread):

    entryStartReading = Signal(str)
    entryFinishedReading = Signal(str, 'QVariantList')
    entryFaultedReading = Signal(str, Exception)

    def __init__(self, filepaths: List[str]) -> None:
        super().__init__()
        self.__filepaths = filepaths

    def run(self) -> None:
        for f in self.__filepaths:
            try:
                self.entryStartReading.emit(f)
                self.entryFinishedReading.emit(f, Parser.load_sheets(f))
            except Exception as e:
                self.entryFaultedReading.emit(f, e)