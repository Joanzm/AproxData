from typing import List
from enum import IntEnum
from .aprox_parser import ADataSetParser

class DataEntry(list):
    """
    Defines a multiple dimension entry of a
    read data set.
    """

    def __init__(self, values: List[float]) -> None:
        if (not values and len(values) < 2):
            raise AttributeError('The minimum dimension of a data entry must be two.')
        super().__init__(values)

    def __getitem__(self, index: int) -> float:
        return super().__getitem__(index)

    def __setitem__(self, index: int, value: float):
        return super().__setitem__(index, value)

    @property
    def dim(self) -> int:
        """
        Getting the dimension of this data entry.
        """
        return len(self)

    @property
    def x(self) -> float:
        """
        Getting the x value of the data entry.
        """
        return self[0]

    @property
    def y(self) -> float:
        """
        Getting the y value of the data entry.
        """
        return self[1]

    @property
    def z(self) -> float:
        """
        Getting the z value of the data set, if
        the dimension is greater or equal to three.
        Else none is returned.
        """
        return self[2] if self.dim > 2 else None

class DataSet(list):
    """
    Defines a data set containing multiple data entries.
    """

    def __init__(self, key: str) -> None:
        super().__init__()
        self._key = key

    @property
    def key(self) -> str:
        return self._key

    def __getitem__(self, index: int) -> DataEntry:
        return super().__getitem__(index)

    def __setitem__(self, index: int, value: DataEntry):
        return super().__setitem__(index, value)

class ProcessState(IntEnum):
    """
    The current state of the read proccess
    for a given DataSet
    """
    Pendeling = 0
    Processing = 1
    Finished = 2
    Faulted = 3

class DataSetReader():
    """
    A abstract wrapper executing the read proccess for a DataSet
    and displaying read status properties.
    
    The _parse method has to be implemented for parsing data e.g.
    from a file or database. The key is the unique identifier for
    the given DataSet.
    """

    def __init__(self, key: str, dataset: DataSet, parser: ADataSetParser) -> None:
        super().__init__()
        self._key = key
        self._dataset = dataset
        self._parser = parser
        self._state = ProcessState.Pendeling
        self._error = None

    @property
    def key(self) -> str:
        return self._key
    
    @property
    def dataset(self) -> DataSet:
        return self._dataset

    @property
    def state(self) -> ProcessState:
        return self._state

    @property
    def error(self) -> Exception:
        return self._error

    def read(self):
        try:
            self.__readerstarted()
            self._dataset.clear()
            self._dataset.extend([DataEntry(val) for val in self._parser.parse(self._key)])
            self.__readerfinished()
        except Exception as e:
            self.__readerfaulted(self, e)

    def __readerstarted(self):
        self._state = ProcessState.Processing
        self._onChange()

    def __readerfinished(self):
        self._state = ProcessState.Finished
        self._onChange()

    def __readerfaulted(self, e: Exception):
        self._state = ProcessState.Faulted
        self._processException = e
        self._onChange()

    def _onChange(self):
        pass
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return self._key == __o
        else:
            return self._key == __o.key

    def __hash__(self) -> int:
        return self._key.__hash__()

    def __str__(self) -> str:
        return "%s: [Key: %s, State: %s, Exception: %s]"%(self.__class__.__name__, self._key, self._state, self._processException)