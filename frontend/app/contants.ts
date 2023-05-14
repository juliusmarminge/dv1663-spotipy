// Python FastAPI running on here
export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

// No sophisticated auth here, just a plain user object in LS and client-side cookie
export const LOCALSTORAGE_KEY = "active_user";
export const COOKIE_NAME = "x-spotipy-user";
