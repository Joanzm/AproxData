from Backend.OcvSoc.Model.ocv_soc_interpolation import OcvSoc2DLinearInterpolation
from Backend.Abstract.ViewModel.abc_vmInterpolation import AbcVmInterpolation

class Vm2DLinearInterpolation(AbcVmInterpolation):

    def __init__(self) -> None:
        super().__init__(OcvSoc2DLinearInterpolation())
