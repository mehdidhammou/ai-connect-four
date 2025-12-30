import { useGameStore } from "@/stores/game-store";
import { ArrowLeft } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";

const GameHeader = () => {
  const reset = useGameStore((state) => state.reset);
  const { solver, name } = useParams();
  return (
    <div className="flex items-center justify-between p-6 border rounded-3xl">
      <div className="flex items-center gap-2 rounded-full">
        <Button
          onClick={reset}
          asChild
          variant={"ghost"}
          className="p-0 mr-2"
          size={"sm"}
        >
          <Link to={"/"}>
            <ArrowLeft />
          </Link>
        </Button>
        <Badge>{solver}</Badge>/<Badge>{name}</Badge>
      </div>
      <div className="flex">
        <Button variant={"destructive"} onClick={reset}>
          Restart
        </Button>
      </div>
    </div>
  );
};

export default GameHeader;
