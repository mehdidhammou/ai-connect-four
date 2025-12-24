import { getFirstMove } from "@/api/move";
import { PIECE, players } from "@/lib/consts";
import { Player, SolverType } from "@/lib/types";
import { useGameStore } from "@/stores/game-store";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";
import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Button } from "../ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";
import { Separator } from "../ui/separator";
import { ToggleGroup, ToggleGroupItem } from "../ui/toggle-group";

const GameStarterSelector = () => {
  const {
    applyMove,
    startingPlayer: startingPlayer,
    setStartingPlayer,
  } = useGameStore();
  const [selectedStarter, setSelectedStarter] = useState<Player>("human");

  const { solver, name } = useParams<{
    solver: SolverType["type"];
    name: string;
  }>();

  const { data: firstMove } = useQuery({
    queryKey: ["firstMove"],
    queryFn: () => getFirstMove({ name: name!, type: solver! } as SolverType),
    enabled: !!solver && !!name,
  });

  const onSelectStarter = () => {
    setStartingPlayer(selectedStarter);
    if (selectedStarter === "cpu" && firstMove) {
      applyMove(firstMove, PIECE.CPU);
    }
  };

  return (
    <Dialog open={!startingPlayer}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Who starts first?</DialogTitle>
        </DialogHeader>
        <ToggleGroup
          variant={"outline"}
          value={selectedStarter}
          onValueChange={(value) => setSelectedStarter(value as Player)}
          defaultValue="human"
          type="single"
          size={"lg"}
          className="grid grid-cols-2"
        >
          {players.map((player) => (
            <ToggleGroupItem
              className="capitalize"
              key={player}
              value={player as string}
            >
              {player}
            </ToggleGroupItem>
          ))}
        </ToggleGroup>
        <Separator />
        <DialogFooter>
          <div className="flex flex-col w-full gap-2">
            <Button disabled={!selectedStarter} onClick={onSelectStarter}>
              Start
            </Button>
            <Button asChild variant={"outline"}>
              <Link to={"/"}>
                <ArrowLeft className="w-4 h-4 mr-2" />
                {"Main menu"}
              </Link>
            </Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default GameStarterSelector;
