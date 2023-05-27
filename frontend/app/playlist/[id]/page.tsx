import { Playlist, Song } from "~/types/models";
import { SongCard } from "~/app/songs/song-card";
import { API_URL, LS_COOKIE_NAME } from "~/lib/contants";
import Link from "next/link";
import { cookies } from "next/headers";
import { getUserPlaylists } from "~/lib/fetch-helpers";

// Don't cache this page
export const dynamic = "force-dynamic";

type PlaylistResponse = {
  id: number;
  name: string;
  owner: string;
  songs: (Song & { artist_name: string })[];
};

export default async function Home(props: { params: { id: string } }) {
  const res = await fetch(`${API_URL}/playlists/${props.params.id}`);
  const playlist = (await res.json()) as PlaylistResponse;

  if (res.status !== 200) {
    return (
      <div className="flex flex-col gap-2 overflow-scroll p-4">
        <h2 className="text-2xl font-bold">Error</h2>
        <p className="text-lg">
          {res.status} {res.statusText}
        </p>
      </div>
    );
  }

  const userPlaylists = await getUserPlaylists();

  return (
    <div className="flex flex-col gap-2 overflow-scroll p-4">
      <div>
        <h2 className="text-2xl font-bold">{playlist.name}</h2>
        <p className="text-foreground/80">by {playlist.owner}</p>
      </div>
      <div className="flex flex-col overflow-scroll">
        {playlist.songs.length === 0 && (
          <>
            <p className="text-foreground/80 text-sm">
              Whoops... It looks like this playlist is empty.
            </p>
            <p className="text-foreground/80 text-sm">
              Consider adding some songs from{" "}
              <Link href="/playlist/1" className="underline">
                the top list
              </Link>
              .
            </p>
          </>
        )}
        {playlist.songs.map((song, idx) => (
          <SongCard
            key={song.id}
            {...song}
            idx={idx + 1}
            currentPlaylistId={playlist.id}
            userPlaylists={userPlaylists}
          />
        ))}
      </div>
    </div>
  );
}
