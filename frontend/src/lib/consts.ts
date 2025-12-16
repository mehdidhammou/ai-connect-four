import { Cpu, User } from "lucide-react";
import { GameMode } from "./types";

export const PIECE = {
    Empty: 0,
    Player: 1,
    Cpu: 2,
} as const;

export const gameModes: GameMode[] = [
    {
        "name": "Human vs CPU (Counting pieces)",
        "link": "/vs-cpu/pieces",
        "Icon1": User,
        "Icon2": User,
    },
    {
        "name": "Human vs CPU (Counting positions)",
        "link": "/vs-cpu/positions",
        "Icon1": User,
        "Icon2": Cpu,
    },
    {
        "name": "CPU vs CPU",
        "link": "/cpu-vs-cpu",
        "Icon1": Cpu,
        "Icon2": Cpu,
    }
]

export const boardShape = {
    rows: 6,
    cols: 7,
}