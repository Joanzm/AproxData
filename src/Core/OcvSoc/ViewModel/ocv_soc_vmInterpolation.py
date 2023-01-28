from PySide6.QtCore import Slot

from ..Model.ocv_soc_interpolation import LinearInterpolation, PolyfitInterpolation
from ...Abstract.ViewModel.abc_vmInterpolation import AbcVmInterpolation

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
        
        if (self._lowerInteropSize < self._interpolation.minInteropSize()):
            self._lowerInteropSize = self._interpolation.minInteropSize()
        if (self._upperInteropSize > self._interpolation.maxInteropSize()):
            self._upperInteropSize = self._interpolation.maxInteropSize()