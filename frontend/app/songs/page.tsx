import { Song } from "~/types/models";
import { SongCard } from "~/components/song-card";
import { API_URL } from "~/lib/contants";
import Link from "next/link";
import { getUserPlaylists } from "../../lib/fetch-helpers";

// Don't cache this page
export const dynamic = "force-dynamic";

type SearchResponse = (Song & { artist_name: string })[];

export default async function Home(props: {
  searchParams: { search: string };
}) {
  const search = props.searchParams.search;
  const res = await fetch(`${API_URL}/songs/?search=${search}`);
  const songs = (await res.json()) as SearchResponse;

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
        <h2 className="text-2xl font-bold">Top results</h2>
      </div>
      <div className="flex flex-col overflow-scroll">
        {songs.length === 0 && (
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
        {songs.map((song, idx) => (
          <SongCard
            key={song.id}
            {...song}
            idx={idx + 1}
            userPlaylists={userPlaylists}
          />
        ))}
      </div>
    </div>
  );
}
