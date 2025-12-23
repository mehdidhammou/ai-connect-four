import { SolverType } from "@/lib/types";

export const getSolvers = async (): Promise<SolverType[]> => {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/solvers`);
    if (!res.ok) throw new Error(`Failed to fetch solvers: ${res.status}`);
    const json = await res.json();
    return json.data as SolverType[];
}