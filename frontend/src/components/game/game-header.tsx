import { useGameStore } from "@/stores/game-store";
import { ArrowLeft, Cpu } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";

const GameHeader = () => {
  const currentPlayer = useGameStore((state) => state.currentPlayer);
  const reset = useGameStore((state) => state.reset);
  const { heuristic } = useParams();
  return (
    <div className="grid items-center grid-cols-4">
      <div className="flex items-center">
        <Button
          onClick={reset}
          asChild
          variant={"ghost"}
          className="mr-2"
          size={"icon"}
        >
          <Link to={"/"}>
            <ArrowLeft />
          </Link>
        </Button>
        <Badge variant={"secondary"} className="capitalize text-md w-fit">
          <Cpu className="mr-2" />
          {heuristic} AI
        </Badge>
      </div>

      <div className="grid col-span-2 place-items-center">
        <h3 className="text-xl font-semibold">{currentPlayer}'s turn</h3>
      </div>

      <div className="flex">
        <Button className="ml-auto" variant={"destructive"} onClick={reset}>
          Restart
        </Button>
      </div>
    </div>
  );
};

export default GameHeader;
