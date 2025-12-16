import { ModelResponse } from "@/lib/types";

export async function getModels(provider: string) {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/models/${provider}`);
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data as ModelResponse;
}