export default async function getApiHealth() {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/ping`);
    if (!res.ok) throw new Error("Network response was not ok");
    return res.json();
}