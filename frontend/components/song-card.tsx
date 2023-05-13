"use client";

import * as React from "react";
import * as Icons from "./icons";
import type { Artist, Song } from "~/types/models";
import { useCurrentSong, useIsPlaying } from "~/app/atoms";
import { twMerge } from "tailwind-merge";

export function SongCard(props: Song & { idx: number } & Artist) {
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
              artist_name: props.name,
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
        <h2 className="hover:underline cursor-pointer">{props.name}</h2>
      </div>
      <button className="group rounded-full flex items-center justify-center w-10">
        <Icons.More className="hidden group-hover:block" />
      </button>
    </div>
  );
}
