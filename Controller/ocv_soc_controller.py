from Model.OcvSoc.ocv_soc_model import OcvSocModel
from View.main_view import MainWindow
from Model.OcvSoc.ocv_soc_celldataparser_xlr import XLRCellDataParser
from threading import Thread
import threading

class OcvSocController():

    def __init__(self) -> None:
        self._view = MainWindow(self.parse_files);
        self._model = OcvSocModel()

    def show_view(self):
        self._view.show()

    def parse_files(self, filename: str) -> Thread:
        return ParserThread(filename)

class ParserThread(Thread):
    def __init__(self, filename: str) -> None:
        super().__init__(daemon=True)
        self.filename = filename

    def run(self) -> None:
        #threading.settrace(trace_function())
        p = XLRCellDataParser()
        p.load_book(self.filename)
        p.load_sheets()

def trace_function(): 
    print("Passing the trace function and current thread is:", str(threading.current_thread().getName()))
