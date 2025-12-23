import { transpose } from "@/lib/utils";
import { useGameStore } from "@/stores/game-store";
import Column from "./column";

const Board = () => {
  const board = useGameStore((state) => state.board);
  return (
    <div className="flex items-center justify-center">
      {transpose(board).map((col, index) => (
        <Column key={index} colIdx={index} column={col} />
      ))}
    </div>
  );
};

export default Board;
