from Backend.OcvSoc.Model.ocv_soc_interpolation import OcvSoc2DLinearInterpolation, TwoDimPolynomialInterpolation
from Backend.Abstract.ViewModel.abc_vmInterpolation import AbcVmInterpolation

class Vm2DInterpolation(AbcVmInterpolation):

    def __init__(self) -> None:
        super().__init__(OcvSoc2DLinearInterpolation())
