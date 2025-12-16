import { PIECE } from "@/lib/consts";
import { Heuristic, Piece } from "@/lib/types";
import { useBoardStore } from "@/stores/board-store";
import { useGameStore } from "@/stores/game-store";
import { useParams } from "react-router-dom";
import Cell from "./cell";

type ColumnProps = {
  column: Piece[];
  colIdx: number;
};

const Column = ({ column, colIdx }: ColumnProps) => {
  const { makeMove, sync, sequence, isSyncing } = useBoardStore();
  const { auto, gameState } = useGameStore();
  const { heuristic } = useParams<{ heuristic: Heuristic }>();
  const disabled =
    isSyncing || column[0] !== PIECE.Empty || auto || gameState !== "CONTINUE";

  const handleClick = async () => {
    if (disabled) {
      return;
    }
    makeMove(colIdx, 1);
    // @ts-expect-error common useParams type
    await sync(heuristic);
  };

  return (
    <button
      disabled={disabled}
      onClick={handleClick}
      className="flex flex-col gap-2 p-2 transition rounded-full enabled:hover:dark:bg-primary enabled:hover:bg-muted"
    >
      {column.map((val, index) => (
        <Cell
          key={index}
          value={val}
          highlight={sequence.some(
            (move) => move.col === colIdx && move.row === index
          )}
        />
      ))}
    </button>
  );
};

export default Column;
