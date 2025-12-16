import { GameState, Player } from "@/lib/types";
import { create } from "zustand";
import { useBoardStore } from "./board-store";


type GameStateStore = {
    currentPlayer: Player,
    gameState: GameState,
    message: string,
    auto: boolean,
}

type GameActionsStore = {
    setMessage: (message: string) => void,
    setGameState: (state: GameState) => void,
    reset: () => void,
    toggleTurn: () => void,
    setCurrentPlayer: (player: Player) => void,
    setAuto: (auto: boolean) => void,
}

export const useGameStore = create<GameStateStore & GameActionsStore>((set, get) => ({
    currentPlayer: undefined,
    gameState: "CONTINUE",
    message: "Continue",
    auto: false,
    reset: () => {
        useBoardStore.getState().reset();
        set({ currentPlayer: undefined, gameState: "CONTINUE", message: "Continue" });
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
    setGameState: (gameState) => set({ gameState }),
}));
