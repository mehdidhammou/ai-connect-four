import Board from "../board";
import { Card, CardContent } from "../ui/card";
import { Separator } from "../ui/separator";
import GameHeader from "./game-header";
import GameOverDialog from "./game-over-dialog";
import GameStarterSelector from "./game-starter-selector";

const Game = () => {
  return (
    <>
      <GameStarterSelector />
      <GameOverDialog />
      <div className="w-full row-span-3">
        <GameHeader />
        <Card className="mt-6">
          <Separator />
          <CardContent className="p-6">
            <Board />
          </CardContent>
        </Card>
      </div>
    </>
  );
};

export default Game;
