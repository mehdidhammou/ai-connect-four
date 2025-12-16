import Board from "../board";
import GameHeader from "./game-header";
import GameOverDialog from "./game-over-dialog";
import StarterSelector from "./starter-selector";
import { Card, CardContent, CardHeader } from "../ui/card";
import { Separator } from "../ui/separator";

const Game = () => {
  return (
    <>
      <StarterSelector players={["Human", "CPU"]} />
      <GameOverDialog />
      <div className="w-full row-span-3">
        <Card >
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

export default Game;
