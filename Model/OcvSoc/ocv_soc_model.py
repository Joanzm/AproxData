from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from Model.Abstract.abc_model import AbcModel
from .ocv_soc_celldata import OcvSocCellData

class OcvSocModel(AbcModel[OcvSocCellData]):
    
    def __init__(self) -> None:
        super().__init__()

    def load_files(self, filenames: List[str]) -> None:
        pass
    
    def get_numpy_array(self) -> None:
        pass
