import { Cpu, User } from "lucide-react";
import { GameMode } from "./types";

export const PIECE = {
    Empty: 0,
    PlayerOne: 1,
    PlayerTwo: 2,
} as const;

export const players = ['human', 'cpu'] as const;

export const gameModes: GameMode[] = [
    {
        "name": "Human vs Pieces Heuristic",
        "link": "/vs-heuristic/pieces",
        "Icon1": User,
        "Icon2": Cpu,
    },
    {
        "name": "Human vs Positions Heuristic",
        "link": "/vs-heuristic/positions",
        "Icon1": User,
        "Icon2": Cpu,
    },
    {
        "name": "Heuristic vs Heuristic",
        "link": "/heuristic-vs-heuristic",
        "Icon1": Cpu,
        "Icon2": Cpu,
    }
]

export const boardShape = {
    rows: 6,
    cols: 7,
}