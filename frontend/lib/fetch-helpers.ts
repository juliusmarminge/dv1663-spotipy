import { cookies } from "next/headers";
import { API_URL, LS_COOKIE_NAME } from "./contants";
import { Playlist } from "~/types/models";

export async function getUserPlaylists() {
  const user = cookies().get(LS_COOKIE_NAME)?.value;
  const playlists = (await fetch(`${API_URL}/playlists`, {
    headers: {
      "Content-Type": "application/json",
      ...(user ? { Authorization: user } : {}),
    },
  }).then((res) => res.json())) as Playlist[];
  const userPlaylists = playlists.filter(
    (p) => p.user_id === JSON.parse(user || "{}").id
  );

  return userPlaylists;
}
