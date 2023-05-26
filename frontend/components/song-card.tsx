"use client";

import * as React from "react";
import * as Icons from "~/components/icons";
import type { Artist, Playlist, Song } from "~/types/models";
import { useCurrentSong, useIsPlaying } from "~/app/atoms";
import { twMerge } from "tailwind-merge";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
  DropdownMenuSeparator,
} from "~/components/dropdown-menu";
import Link from "next/link";
import { API_URL, LS_COOKIE_NAME } from "~/app/contants";
import { useRouter } from "next/navigation";

export function SongCard(
  props: Song & { idx: number; artist_name: string; userPlaylists: Playlist[] }
) {
  const { song, setSong } = useCurrentSong();
  const { isPlaying, setIsPlaying } = useIsPlaying();

  const thisIsActive = props.id === song?.id;
  const thisIsPlaying = thisIsActive && isPlaying;

  return (
    <div className="flex p-2 gap-4 hover:bg-background transition-colors group rounded hover:text-foreground-muted">
      <div className="w-8 flex items-center justify-center">
        <button
          onClick={() => {
            if (thisIsPlaying) {
              setIsPlaying(false);
              return;
            }
            setSong({
              id: props.id,
              title: props.title,
              artist_name: props.artist_name,
              cover_path: props.cover_path,
              mp3_path: props.mp3_path,
            });
          }}
        >
          {thisIsPlaying ? (
            <Icons.Pause className="h-4 w-4 hidden group-hover:block" />
          ) : (
            <Icons.Play className="h-4 w-4 hidden group-hover:block" />
          )}
        </button>
        <span className="block group-hover:hidden select-none">
          {props.idx}
        </span>
      </div>
      <img
        src={props.cover_path}
        className="h-12 w-12 rounded-sm select-none"
      />
      <div className="flex-1 flex flex-col w-[60ch]">
        <h1
          className={twMerge(
            "text-xl font-bold",
            thisIsActive && "text-primary"
          )}
        >
          {props.title}
        </h1>
        <Link
          href={`/artist/${props.artist_id}`}
          className="hover:underline cursor-pointer"
        >
          {props.artist_name}
        </Link>
      </div>

      <SongActions
        songId={props.id}
        artistId={props.artist_id}
        userPlaylists={props.userPlaylists}
      />
    </div>
  );
}

function SongActions(props: {
  songId: Song["id"];
  artistId: Artist["id"];
  userPlaylists: Playlist[];
}) {
  const router = useRouter();

  async function addToPlaylist(playlistId: number) {
    const user = localStorage.getItem(LS_COOKIE_NAME);
    const res = await fetch(
      `${API_URL}/playlists/${playlistId}/${props.songId}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          ...(user ? { Authorization: user } : {}),
        },
      }
    );

    if (!res.ok) {
      const json = await res.json();
      alert(json.message);
    }
    router.refresh();
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger>
        <Icons.More className="hidden group-hover:block" />
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-[225px]">
        <DropdownMenuItem asChild>
          <Link href={`/artist/${props.artistId}`}>Go to artist</Link>
        </DropdownMenuItem>
        <DropdownMenuItem disabled>Go to album</DropdownMenuItem>

        <DropdownMenuSeparator />

        <DropdownMenuSub>
          <DropdownMenuSubTrigger>Add to Playlist</DropdownMenuSubTrigger>
          <DropdownMenuSubContent>
            {props.userPlaylists.map((playlist) => (
              <DropdownMenuItem
                key={playlist.id}
                onClick={() => addToPlaylist(playlist.id)}
              >
                {playlist.name}
              </DropdownMenuItem>
            ))}
          </DropdownMenuSubContent>
        </DropdownMenuSub>

        <DropdownMenuItem disabled>
          Remove from playlist
          <Icons.Trash className="ml-auto h-4 w-4" />
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
