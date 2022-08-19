from ..Model.ocv_soc_entry import OcvSocEntry
from ...Abstract.ViewModel.abc_celldatagraph import AbcCellDataGraph

class OcvSocCellDataGraph(AbcCellDataGraph[OcvSocEntry]):

    def __init__(self) -> None:
        super().__init__()