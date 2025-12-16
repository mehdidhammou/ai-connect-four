import { LucideIcon } from "lucide-react";
import { PIECE } from "./consts";

export type GameMode = {
    name: string,
    link: string,
    Icon1: LucideIcon,
    Icon2: LucideIcon,
};

export type GameState = "CONTINUE" | "WIN" | "LOSE" | "TIE" | "MM_POS_WIN" | "MM_PIECE_WIN";

export type ObjectValues<T> = T[keyof T];

export type Piece = ObjectValues<typeof PIECE>;

export type Heuristic = "pieces" | "positions";

export type Player = "Human" | "CPU" | Heuristic | undefined;

export type Move = {
    row: number,
    col: number,
};

export type GameResponse = {
    success: boolean,
    board: Piece[][],
    message: string,
    state: GameState,
    sequence: Move[],
};

export type Model = {
    name: string,
    description: string,
};

export type ModelResponse = {
    data: Model[],
};


