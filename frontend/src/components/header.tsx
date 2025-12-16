import ConnectedBadge from "./connected-badge";
import { ModeToggle } from "./mode-toggle";
export default function Header() {
  return (
    <header className="flex flex-col gap-4">
      <div className="flex items-start justify-between w-full">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold">Connect Four</h1>
          <div>
            <ConnectedBadge />
          </div>
          <p className="text-muted-foreground">
            A classic two-player connection game where the objective is to be
            the first to connect four of your pieces in a row. Challenge two
            heuristics or play against Mistral's LLMs.
          </p>
        </div>
        <div>
          <ModeToggle />
        </div>
      </div>
    </header>
  );
}
