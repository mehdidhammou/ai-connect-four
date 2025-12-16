import { GameResponse, Heuristic, Piece, Move } from '@/lib/types'
import { createEmptyBoard, transpose } from '@/lib/utils'
import { create } from 'zustand'
import { PIECE } from '../lib/consts'
import { useGameStore } from './game-store'


type boardState = {
    board: Piece[][],
    sequence: Move[],
    isSyncing: boolean,
}

const initialBoardState: boardState = {
    board: createEmptyBoard(),
    sequence: [],
    isSyncing: false,
}

type boardActions = {
    makeMove: (col: number, piece: Piece) => Promise<void>,
    sync: (heuristic: Heuristic) => Promise<void>,
    setIsSyncing: (isSyncing: boolean) => void,
    reset: () => void,
}

export const useBoardStore = create<boardState & boardActions>()((set, get) => ({
    ...initialBoardState,
    makeMove: async (col, piece) => {

        const newBoard = transpose(get().board);

        const row = newBoard[col].lastIndexOf(PIECE.Empty);
        if (row === -1) return;
        newBoard[col][row] = piece;

        set({ board: transpose(newBoard) })

        useGameStore.getState().toggleTurn();
    },
    setIsSyncing: (isSyncing) => set({ isSyncing }),
    sync: async (heuristic) => {
        set({ isSyncing: true });
        try {
            const res = await fetch(
                `${import.meta.env.VITE_API_BASE_URL}/${useGameStore.getState().auto ? "get_move" : "make_move"}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        heuristic: useGameStore.getState().auto ? useGameStore.getState().currentPlayer : heuristic,
                        board: get().board,
                    }),
                }
            );

            const data = await res.json() as GameResponse;
            set({ board: data.board, sequence: data.sequence });
            if (data.state !== "CONTINUE") {
                await new Promise((resolve) => setTimeout(resolve, 500));
                useGameStore.setState({ gameState: data.state, message: data.message });
            }
            useGameStore.getState().toggleTurn();

        } catch (error) {
            console.error("Error handling player move:", error);
            alert("couldn't connect to the server");
        }
        set({ isSyncing: false });
    },
    reset: () => {
        set(initialBoardState)
    },
}))