import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { PIECE, boardShape } from "./consts";
import { Piece } from "./types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function transpose(matrix: Piece[][]): Piece[][] {
  return matrix[0].map((_, colIndex) => matrix.map((row) => row[colIndex]));
}

export function restart() {
  window.location.reload();
}

export function createEmptyBoard(rows: number = boardShape.rows, cols: number = boardShape.cols): Piece[][] {
  return Array(rows)
    .fill(0)
    .map(() => Array<Piece>(cols)
      .fill(PIECE.Empty));
}
