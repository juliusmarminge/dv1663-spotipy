import { Playlist } from "~/types/models";
import { CreatePlaylistForm } from "~/components/playlist-form";
import { API_URL, LS_COOKIE_NAME } from "~/app/contants";
import { cookies } from "next/headers";
import Link from "next/link";

export async function Playlists() {
  const user = cookies().get(LS_COOKIE_NAME)?.value;

  const res2 = await fetch(`${API_URL}/playlists/`, {
    headers: {
      "Content-Type": "application/json",
      // append the current user if they're logged in
      ...(user ? { Authorization: user } : {}),
    },
  });
  const playlists = (await res2.json()) as Playlist[];

  return (
    <div className="p-4 rounded-lg space-y-4 bg-background-muted h-full w-72">
      <h2 className="text-2xl font-bold">Playlists</h2>
      {user && <CreatePlaylistForm user={user} />}
      <div className="flex flex-col">
        {playlists.map((playlist) => (
          <PlaylistListItem key={playlist.id} playlist={playlist} />
        ))}
      </div>
    </div>
  );
}

function PlaylistListItem(props: { playlist: Playlist }) {
  return (
    <Link
      href={`/playlist/${props.playlist.id}`}
      className="hover:bg-background p-2 rounded"
    >
      <span>{props.playlist.name}</span>
    </Link>
  );
}
