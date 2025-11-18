from .heuristic import Heuristic
from .count_pieces_heuristic import CountPiecesHeuristic
from .count_positions_heuristic import CountPositionsHeuristic


class HeuristicFactory:
    @staticmethod
    def create_heuristic(heuristic: str) -> Heuristic:
        match heuristic:
            case "pieces":
                return CountPiecesHeuristic(id=1)
            case "positions":
                return CountPositionsHeuristic(id=2)
            case _:
                raise Exception("Heuristic not found!")
