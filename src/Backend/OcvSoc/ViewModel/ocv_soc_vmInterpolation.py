from PySide6.QtCore import Slot

from Backend.OcvSoc.Model.ocv_soc_interpolation import LinearInterpolation, PolyfitInterpolation
from Backend.Abstract.ViewModel.abc_vmInterpolation import AbcVmInterpolation

class Vm2DInterpolation(AbcVmInterpolation):

    def __init__(self) -> None:
        super().__init__(LinearInterpolation())

    @Slot(str)
    def changeAlgorithm(self, value: str):
        self.onClearView()
        if value == "Linear Interpolation":
            self._interpolation = LinearInterpolation()
        if value == "Polyfit Interpolation":
            self._interpolation = PolyfitInterpolation()