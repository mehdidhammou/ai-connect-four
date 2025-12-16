import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useGameStore } from "@/stores/game-store";
import { Separator } from "@radix-ui/react-separator";
import { AlertCircle, CheckCircle } from "lucide-react";
import { Button } from "../ui/button";

const GameOverDialog = () => {
  const gameState = useGameStore((state) => state.gameState);
  const message = useGameStore((state) => state.message);
  const reset = useGameStore((state) => state.reset);

  if (gameState === "CONTINUE") return null;

  return (
    <Dialog defaultOpen>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Game over</DialogTitle>
        </DialogHeader>
        {gameState === "WIN" ? (
          <div className="flex flex-col items-center justify-center gap-4 p-8 text-green-600 bg-green-100 rounded-md text-md">
            <CheckCircle />
            <p className="font-bold">{message}</p>
          </div>
        ) : gameState === "LOSE" ? (
          <div className="flex flex-col items-center justify-center gap-4 p-8 text-red-600 bg-red-100 rounded-md text-md">
            <AlertCircle />
            <p className="font-bold">{message}</p>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center gap-4 p-8 text-yellow-600 bg-yellow-100 rounded-md text-md">
            <p className="font-bold">{message}</p>
          </div>
        )}
        <Separator />
        <DialogFooter>
          <Button className="w-full" onClick={reset}>
            Restart
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default GameOverDialog;
