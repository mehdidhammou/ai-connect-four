import { LucideIcon } from "lucide-react";
import { PIECE, players } from "./consts";

export type GameMode = {
    name: string,
    link: string,
    Icon1: LucideIcon,
    Icon2: LucideIcon,
};

export type GameState = "CONTINUE" | "WIN" | "LOSE" | "TIE";

export type ObjectValues<T> = T[keyof T];

export type Piece = ObjectValues<typeof PIECE>;

export type Board = Piece[][];

export type HeuristicName = "pieces" | "positions";

export type ModelProviderName = "mistral";

export type Player = typeof players[number];

export type Move = {
    row: number,
    col: number,
};

export interface HeuristicSolver {
    type: "heuristic";
    name: HeuristicName;
}

export interface LLMSolver {
    type: ModelProviderName;
    name: string;
}

export type SolverType = HeuristicSolver | LLMSolver;

export type MoveRequest = {
    board: Board,
    starting_player: Player,
    player_move: Move,
    solver: SolverType,
};

export type MoveResponse = {
    state: GameState,
    solver_move: Move | null,
    winning_sequence: Move[] | null,
}
