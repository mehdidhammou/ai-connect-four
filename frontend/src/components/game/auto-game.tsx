import Board from "../board";
import GameHeader from "./game-header";
import GameOverDialog from "./game-over-dialog";
import StarterSelector from "./starter-selector";
import { Card, CardContent, CardHeader } from "../ui/card";
import { Separator } from "../ui/separator";
import { useGameStore } from "@/stores/game-store";
import { useEffect } from "react";
import { useBoardStore } from "@/stores/board-store";
import { useParams } from "react-router-dom";
import { Heuristic } from "@/lib/types";

const AutoGame = () => {
  const setAuto = useGameStore((state) => state.setAuto);
  const gameState = useGameStore((state) => state.gameState);
  const sync = useBoardStore((state) => state.sync);
  const currentPlayer = useGameStore((state) => state.currentPlayer);
  const { heuristic } = useParams();
  useEffect(() => {
    setAuto(true);
    let id: number;
    if (gameState === "CONTINUE" && currentPlayer) {
      id = setInterval(async () => await sync(heuristic as Heuristic), 500);
    }
    return () => {
      clearInterval(id);
      setAuto(false);
    };
  }, [currentPlayer, gameState, heuristic, setAuto, sync]);

  return (
    <>
      <StarterSelector players={["pieces", "positions"]} />
      <GameOverDialog />
      <div className="w-full row-span-3">
        <Card>
          <CardHeader>
            <GameHeader />
          </CardHeader>
          <Separator />
          <CardContent className="p-6">
            <Board />
          </CardContent>
        </Card>
      </div>
    </>
  );
};

export default AutoGame;
