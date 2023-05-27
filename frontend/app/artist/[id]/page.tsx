import { Playlist, Song } from "~/types/models";
import { SongCard } from "~/components/song-card";
import { API_URL, LS_COOKIE_NAME } from "~/app/contants";
import Link from "next/link";
import { cookies } from "next/headers";

// Don't cache this page
export const dynamic = "force-dynamic";

type PlaylistResponse = {
  id: number;
  name: string;
  biography: string;
  songs: Song[];
};

export default async function ArtistPage(props: { params: { id: string } }) {
  const res = await fetch(`${API_URL}/artists/${props.params.id}`);
  const artist = (await res.json()) as PlaylistResponse;

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

  return (
    <div className="flex flex-col gap-2 overflow-scroll p-4">
      <div>
        <h2 className="text-2xl font-bold">{artist.name}</h2>
        <p className="text-foreground/80">{artist.biography}</p>
      </div>
      <div className="flex flex-col overflow-scroll">
        {artist.songs.length === 0 && (
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
        {artist.songs.map((song, idx) => (
          <SongCard
            key={song.id}
            {...song}
            artist_name={artist.name}
            idx={idx + 1}
            userPlaylists={userPlaylists}
          />
        ))}
      </div>
    </div>
  );
}
