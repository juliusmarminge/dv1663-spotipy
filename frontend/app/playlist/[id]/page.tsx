import { Artist, Song } from "~/types/models";
import * as Icons from "~/components/icons";

// Python FastAPI running on here
const API_URL = "http://127.0.0.1:8000";

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

function SongCard(props: Song & { idx: number } & Artist) {
  console.log(props);
  return (
    <div className="flex p-2 gap-4 hover:bg-background transition-colors group rounded hover:text-foreground-muted">
      <div className="w-8 flex items-center justify-center">
        <Icons.Play className="h-4 w-4 hidden group-hover:block" />
        <span className="block group-hover:hidden select-none">
          {props.idx}
        </span>
      </div>
      <img
        src={props.cover_path}
        className="h-12 w-12 rounded-sm select-none"
      />
      <div className="flex-1 flex flex-col w-[60ch]">
        <h1 className="text-xl font-bold">{props.title}</h1>
        <h2 className="hover:underline cursor-pointer">{props.name}</h2>
        <audio src="">helllo</audio>
        <figure>
          <figcaption>Listen to the T-Rex:</figcaption>
          <audio
            controls
            src={`http://127.0.0.1:8000/static/${props.mp3_path}`}
          >
            <a href={`http://127.0.0.1:8000/static/${props.mp3_path}`}>
              Download audio
            </a>
          </audio>
        </figure>
      </div>
      <button className="group rounded-full flex items-center justify-center w-10">
        <Icons.More className="hidden group-hover:block" />
      </button>
    </div>
  );
}
