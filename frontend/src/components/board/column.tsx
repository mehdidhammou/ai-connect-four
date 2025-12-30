import { makeMove } from "@/api/move";
import { PIECE } from "@/lib/consts";
import { MoveRequest, Piece, SolverType } from "@/lib/types";
import { useGameStore } from "@/stores/game-store";
import { useMutation } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import Cell from "./cell";
import { getMoveFromColIdx } from "@/lib/utils";

type ColumnProps = {
  column: Piece[];
  colIdx: number;
};

const Column = ({ column, colIdx }: ColumnProps) => {
  const { board, gameState, setGameState, startingPlayer, applyMove } =
    useGameStore();

  const { solver, name } = useParams<{
    solver: SolverType["type"];
    name: string;
  }>();

  const { mutate, data, isPending } = useMutation({
    mutationFn: makeMove,
    onSuccess: async (data) => {
      setGameState(data.state);
      applyMove(getMoveFromColIdx(board, colIdx)!, PIECE.HUMAN);
      await new Promise((resolve) => setTimeout(resolve, 50));
      applyMove(data.solver_move!, PIECE.CPU);
    },
  });

  const disabled =
    isPending ||
    column[0] !== PIECE.EMPTY ||
    gameState !== "CONTINUE" ||
    !startingPlayer ||
    !solver ||
    !name;

  const handleClick = () => {
    if (disabled) return;
    const moveRequest: MoveRequest = {
      board: board,
      player_move: getMoveFromColIdx(board, colIdx)!,
      starting_player: startingPlayer!,
      solver: {
        type: solver!,
        name: name!,
      } as SolverType,
    };
    mutate(moveRequest);
  };

  return (
    <button
      disabled={disabled}
      onClick={handleClick}
      className="flex flex-col flex-1 gap-2 p-2 transition rounded-full enabled:hover:dark:bg-primary enabled:hover:bg-muted md:flex-none"
    >
      {column.map((val, index) => (
        <Cell
          key={index}
          value={val}
          highlight={
            data?.winning_sequence?.some(
              (move) => move.col === colIdx && move.row === index
            ) || false
          }
        />
      ))}
    </button>
  );
};

export default Column;
