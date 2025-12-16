from src.types.move import Move


class ConnectFourBoard:
    def __init__(self, initial_state: list[list[int]] | None = None):
        self.rows = 6
        self.cols = 7
        self.winning_sequence: list[Move] | None = None
        self.state = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        if initial_state:
            if len(initial_state) != self.rows or len(initial_state[0]) != self.cols:
                raise ValueError(
                    f"Initial state shape is incorrect. Expected shape: ({self.rows}, {self.cols})"
                )
            else:
                self.state = [[_ for _ in row] for row in initial_state]

    def make_move(self, move: Move, piece: int) -> None:
        if move not in self.get_possible_moves():
            raise ValueError("Invalid move")

        self.state[move["row"]][move["col"]] = piece

    def get_possible_moves(self) -> list[Move]:
        moves: list[Move] = []
        for col in range(self.cols):
            for row in range(self.rows - 1, -1, -1):
                if self.state[row][col] == 0:
                    moves.append({"col": col, "row": row})
                    break
        return moves

    def has_won(self, piece: int) -> bool:
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (-1, 1),
        ]  # Right, Down, Diagonal ↘, Diagonal ↗

        for row in range(self.rows):
            for col in range(self.cols):
                if self.state[row][col] != piece:
                    continue

                for dr, dc in directions:
                    if all(
                        0 <= row + dr * i < self.rows
                        and 0 <= col + dc * i < self.cols
                        and self.state[row + dr * i][col + dc * i] == piece
                        for i in range(4)
                    ):
                        self.winning_sequence = [
                            Move(row=row + dr * i, col=col + dc * i) for i in range(4)
                        ]
                        return True

        return False
