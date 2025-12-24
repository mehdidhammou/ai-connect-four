import { Move, MoveRequest, MoveResponse, SolverType } from "@/lib/types";

export const makeMove = async (moveRequest: MoveRequest): Promise<MoveResponse> => {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/move/${moveRequest.solver.type}/${moveRequest.solver.name}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(moveRequest),
    });

    if (!res.ok) {
        throw new Error(`Failed to make move: ${res.status}`);
    }

    const data = await res.json();
    return data.data;
}

export const getFirstMove = async (solver: SolverType): Promise<Move> => {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/first-move/${solver.type}/${solver.name}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error(`Failed to get first move: ${res.status}`);
    }
    const data = await res.json();
    return data.data;
}