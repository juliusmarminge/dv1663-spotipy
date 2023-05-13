import { Artist, Song } from "~/types/models";
import { SongCard } from "~/components/song-card";
import { API_URL } from "~/app/contants";

// Don't cache this page
export const dynamic = "force-dynamic";

export default async function Home(props: { params: { id: string } }) {
  const res = await fetch(`${API_URL}/songs`);
  const songs = (await res.json()) as (Song & Artist)[];

  return (
    <div className="flex flex-col gap-2 overflow-scroll p-4">
      <h2 className="text-2xl font-bold">{props.params.id}</h2>
      <div className="flex flex-col overflow-scroll">
        {songs.map((song, idx) => (
          <SongCard key={song.id} {...song} idx={idx + 1} />
        ))}
      </div>
    </div>
  );
}
