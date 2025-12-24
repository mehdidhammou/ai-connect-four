import { PIECE } from "@/lib/consts";
import { Board, GameState, Move, Piece, Player } from "@/lib/types";
import { createEmptyBoard } from "@/lib/utils";
import { create } from "zustand";


type GameStateStore = {
    board: Board,
    gameState: GameState,
    startingPlayer: Player | undefined,
}

const getInitialGameState = (): GameStateStore => ({
    board: createEmptyBoard(),
    gameState: "CONTINUE",
    startingPlayer: undefined,
})

type GameActionsStore = {
    applyMove: (move: Move, piece: Piece) => void,
    reset: () => void,
    setGameState: (state: GameState) => void,
    setStartingPlayer: (player: Player) => void,
    isBoardEmpty: () => boolean,
}

export const useGameStore = create<GameStateStore & GameActionsStore>((set, get) => ({
    ...getInitialGameState(),
    applyMove: (move: Move, piece: Piece) => set((state) => {
        const newBoard = state.board.map((row) => [...row]);
        newBoard[move.row][move.col] = piece;
        return { board: newBoard };
    }),
    setStartingPlayer: (player: Player) => set({ startingPlayer: player }),
    setGameState: (state: GameState) => set({ gameState: state }),
    reset: () => set(getInitialGameState()),
    isBoardEmpty: () => {
        return get().board.every(row => row.every(cell => cell === PIECE.EMPTY));
    }
}));
