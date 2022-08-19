from .ocv_soc_vmData import OcvSocDataViewModel, OcvSocCellData
from Backend.Abstract.ViewModel.abc_vmCellDataGraph import AbcCellDataGraph

class OcvSocCellDataGraph(AbcCellDataGraph[OcvSocDataViewModel, OcvSocCellData]):

    def __init__(self, model: OcvSocDataViewModel) -> None:
        super().__init__(model)