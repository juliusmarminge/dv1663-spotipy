import { SongCard } from "~/components/song-card";
import { Song } from "~/types/models";
import { PlaylistForm } from "./create-playlist";

// Python FastAPI running on here
const API_URL = "http://127.0.0.1:8000";

// Don't cache this page
export const dynamic = "force-dynamic";

export default async function Home() {
  const res = await fetch(`${API_URL}/songs`);
  const songs = (await res.json()) as Song[];

  const res2 = await fetch(`${API_URL}/playlists`);
  const playlists = (await res2.json()) as any[];

  return (
    <main className="flex min-h-screen flex-col items-center p-24 gap-8">
      <h1 className="text-6xl font-bold">Spotipy</h1>
      <PlaylistForm />
      <div className="flex gap-8">
        <div>
          <h2 className="text-2xl font-bold">Playlists</h2>
          <div className="flex flex-col gap-4">
            {playlists.map((playlist) => (
              <div key={playlist.id}>{playlist.name}</div>
            ))}
          </div>
        </div>
        <div className="flex flex-col gap-4">
          {songs.map((song) => (
            <SongCard key={song.id} {...song} />
          ))}
        </div>
      </div>
    </main>
  );
}
