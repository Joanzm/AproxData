from typing import List
from PySide6.QtCore import QThread, Signal

from ..OcvSoc import ocv_soc_celldataparser_xlr as Parser

class LoadXlsFileWorker(QThread):

    entry_startReading = Signal(str)
    entry_finishedReading = Signal(str, 'QVariantList')
    entry_faultedReading = Signal(str, Exception)

    def __init__(self, filepaths: List[str]) -> None:
        super().__init__()
        self.__filepaths = filepaths

    def run(self) -> None:
        for f in self.__filepaths:
            try:
                self.entry_startReading.emit(f)
                self.entry_finishedReading.emit(f, Parser.load_sheets(f))
            except Exception as e:
                self.entry_faultedReading.emit(f, e)