from PySide6.QtCore import QPointF, Signal, Property

from Backend.Abstract.Model.abc_entry import AbcEntry

class OcvSocEntry(AbcEntry):
    """
    Defines a model class for a reference between
    a OCV (open circuit voltage) and a SOC
    (state of charge) value.
    """

    voltageChanged = Signal(float)
    socChanged = Signal(float)

    def __init__(self) -> None:
        super().__init__()

    def __init__(self, voltage: float, soc: float) -> None:
        super().__init__()
        self._voltage = voltage
        self._soc = soc
    
    @Property(float, notify=voltageChanged)
    def voltage(self):
        """
        Getting the voltage value of this entry.
        """
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        """
        Settings the voltage value of this entry.
        Voltage must be greater or equal to zero.
        """
        if value < 0:
            raise ValueError(f'Voltage lower than zero: {value}')
        else:
            self._voltage = value
            self.voltageChanged.emit(value)

    @Property(float, notify=socChanged)
    def soc(self):
        """
        Getting the soc value of this entry.
        """
        return self._soc

    @soc.setter
    def soc(self, value):
        """
        Allow all soc values. Can be negativ
        or greater than 1, if cell is not in norm.
        But should not be greater than 1.2 and lower
        than -0.2.
        """
        if value < -0.2:
            raise ValueError(f'Voltage lower than -0.2: {value}')
        if value > 1.2:
            raise ValueError(f'Voltage greater than 1.2: {value}')
        else:
            self._soc = value
            self.socChanged.emit(value)
    
    @Property(QPointF)
    def point(self) -> QPointF:
        p = QPointF(self._voltage, self._soc)
        return p

    def __hash__(self) -> int:
        return self.voltage.__hash__() ^ self.soc.__hash__()
    
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, OcvSocEntry) and self.voltage == __o.voltage and self.soc == __o.soc

    def __str__(self) -> str:
        return f'OvcSocEntry: ({self.voltage}, {self.soc})'