import { Song } from "~/types/models";

export function SongCard(props: Song) {
  return (
    <div className="flex p-4 gap-4 bg-zinc-800 hover:bg-zinc-900 transition-colors rounded-lg">
      <img src={props.cover_path} className="h-16 w-16 rounded" />
      <div className="flex-1 flex flex-col w-[60ch]">
        <h1 className="text-xl font-bold">{props.title}</h1>
        <h2>{props.artist}</h2>
      </div>
      <button className="group p-2 hover:bg-zinc-800/80">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="h-10 w-10 group-hover:text-green-500"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <polygon points="10 8 16 12 10 16 10 8"></polygon>
        </svg>
      </button>
    </div>
  );
}
