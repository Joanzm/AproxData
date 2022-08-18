from .ocv_soc_entry import OcvSocEntry
from Model.Abstract.abc_celldatagraph import AbcCellDataGraph

class OcvSocCellDataGraph(AbcCellDataGraph[OcvSocEntry]):

    def __init__(self) -> None:
        super().__init__()