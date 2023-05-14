import { Artist, Song } from "~/types/models";
import { SongCard } from "~/components/song-card";
import { API_URL } from "~/app/contants";

// Don't cache this page
export const dynamic = "force-dynamic";

type PlaylistResponse = {
  id: string;
  name: string;
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

  return (
    <div className="flex flex-col gap-2 overflow-scroll p-4">
      <h2 className="text-2xl font-bold">{playlist.name}</h2>
      <div className="flex flex-col overflow-scroll">
        {playlist.songs.map((song, idx) => (
          <SongCard key={song.id} {...song} idx={idx + 1} />
        ))}
      </div>
    </div>
  );
}
