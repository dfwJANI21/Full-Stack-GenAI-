const rawBaseUrl = import.meta.env.VITE_API_URL || "/api";
export const API_BASE_URL = rawBaseUrl.endsWith("/") ? rawBaseUrl.slice(0, -1) : rawBaseUrl;

