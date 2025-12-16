import { transpose } from "@/lib/utils";
import Column from "./column";
import { useBoardStore } from "@/stores/board-store";

const Board = () => {
  const board = useBoardStore((state) => state.board);
  return (
    <div className="flex items-center justify-center">
      {transpose(board).map((col, index) => (
        <Column key={index} colIdx={index} column={col} />
      ))}
    </div>
  );
};

export default Board;
