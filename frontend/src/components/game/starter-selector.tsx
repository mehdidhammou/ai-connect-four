import { PIECE } from "@/lib/consts";
import { Player } from "@/lib/types";
import { useBoardStore } from "@/stores/board-store";
import { useGameStore } from "@/stores/game-store";
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

const StarterSelector = ({ players }: { players: Player[] }) => {
  const makeMove = useBoardStore((state) => state.makeMove);

  const { currentPlayer, setCurrentPlayer } = useGameStore();
  const [selectedStarter, setSelectedStarter] = useState<Player>();
  // @ts-expect-error Typical react router param type inference error
  const { heuristic } = useParams<{ heuristic: Heuristic }>();

  const handleStartClick = () => {
    setCurrentPlayer(selectedStarter);
    if (selectedStarter === "CPU") {
      switch (heuristic) {
        case "PIECES":
          makeMove(0, PIECE.Cpu);
          break;
        case "POSITIONS":
          makeMove(3, PIECE.Cpu);
          break;
      }
    }
  };

  return (
    <Dialog open={!currentPlayer}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Who starts first?</DialogTitle>
        </DialogHeader>
        <ToggleGroup
          variant={"outline"}
          value={selectedStarter}
          onValueChange={(value) => setSelectedStarter(value as Player)}
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
            <Button disabled={!selectedStarter} onClick={handleStartClick}>
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

export default StarterSelector;
