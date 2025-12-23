import { GameState } from "./types";

export const PIECE = {
    EMPTY: 0,
    HUMAN: 1,
    CPU: 2,
} as const;

export const players = ['human', 'cpu'] as const;

export const boardShape = {
    rows: 6,
    cols: 7,
}

export const gameStateMessages: Record<Exclude<GameState, "CONTINUE">, string> = {
    TIE: "It's a tie!",
    WIN: "You win!",
    LOSE: "You lose!",
}