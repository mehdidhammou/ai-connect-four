import { Board, GameState, Move, Player } from "@/lib/types";
import { create } from "zustand";
import { useBoardStore } from "./board-store";


type GameStateStore = {
    currentPlayer: 1 | 2 | undefined,
    board: Board,
    state: GameState,
    winningSequence: Move[] | null,
    auto: boolean, 
}

type GameActionsStore = {
    setMessage: (message: string) => void,
    setState: (state: GameState) => void,
    reset: () => void,
    toggleTurn: () => void,
    setCurrentPlayer: (player: Player) => void,
    setAuto: (auto: boolean) => void,
}

export const useGameStore = create<GameStateStore & GameActionsStore>((set, get) => ({
    currentPlayer: undefined,
    state: "CONTINUE",
    message: "Continue",
    auto: false,
    reset: () => {
        useBoardStore.getState().reset();
        set({ currentPlayer: undefined, state: "CONTINUE", message: "Continue" });
    },
    setAuto: (auto) => set({ auto }),
    toggleTurn: () => {
        let nextPlayer: Player;
        if (get().auto) {
            nextPlayer = get().currentPlayer === "pieces" ? "positions" : "pieces";
        } else {
            nextPlayer = get().currentPlayer === "CPU" ? "Human" : "CPU";
        }
        set({ currentPlayer: nextPlayer })
    },
    setCurrentPlayer: (player) => set({ currentPlayer: player }),
    setMessage: (message) => set({ message }),
    setState: (gameState) => set({ state: gameState }),
}));
