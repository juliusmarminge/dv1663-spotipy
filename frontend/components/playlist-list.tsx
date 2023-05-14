import { Playlist } from "~/types/models";
import { CreatePlaylistForm } from "~/components/playlist-form";
import { API_URL } from "~/app/contants";

export async function Playlists() {
  const res2 = await fetch(`${API_URL}/playlists`);
  const playlists = (await res2.json()) as Playlist[];

  return (
    <div className="p-4 rounded-lg max-w-sm space-y-4 bg-background-muted h-full">
      <h2 className="text-2xl font-bold">Your Playlists</h2>
      <CreatePlaylistForm />
      <div className="flex flex-col gap-4">
        {playlists.map((playlist) => (
          <div key={playlist.id}>{playlist.name}</div>
        ))}
      </div>
    </div>
  );
}