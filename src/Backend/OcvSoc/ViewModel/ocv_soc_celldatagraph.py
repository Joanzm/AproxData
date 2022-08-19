from ..Model.ocv_soc_model import OcvSocModel, OcvSocCellData
from ...Abstract.ViewModel.abc_celldatagraph import AbcCellDataGraph

class OcvSocCellDataGraph(AbcCellDataGraph[OcvSocModel, OcvSocCellData]):

    def __init__(self, model: OcvSocModel) -> None:
        super().__init__(model)