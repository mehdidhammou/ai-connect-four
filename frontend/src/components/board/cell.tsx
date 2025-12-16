import { Piece } from "@/lib/types";
import { cn } from "@/lib/utils";

type CellProps = {
  value: Piece;
  highlight: boolean;
};

const Cell = ({ value, highlight = false }: CellProps) => {
  const colorClass =
    value === 1 ? "bg-red-400" : value === 2 ? "bg-yellow-400" : "bg-zinc-500";
  return (
    <div
      className={cn(
        "w-16 h-16 rounded-full",
        colorClass,
        highlight && "border-4 border-green-500"
      )}
    />
  );
};

export default Cell;
