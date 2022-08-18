from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar("T")

class AbcModel(ABC, Generic[T]):

    def __init__(self) -> None:
        super().__init__()
        self.celldata = []

    @abstractmethod
    def load_files(self, filenames: List[str]) -> None:
        pass

    @abstractmethod
    def get_numpy_array(self) -> None:
        pass


