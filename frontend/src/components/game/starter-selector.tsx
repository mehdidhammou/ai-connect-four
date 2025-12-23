import { Player } from "@/lib/types";
import { useGameStore } from "@/stores/game-store";
import { ArrowLeft } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
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
import { players } from "@/lib/consts";

const StarterSelector = () => {
  const { currentPlayer, setCurrentPlayer } = useGameStore();
  const [selectedStarter, setSelectedStarter] = useState<Player>("human");

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
            <Button
              disabled={!selectedStarter}
              onClick={() => setCurrentPlayer(selectedStarter)}
            >
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
