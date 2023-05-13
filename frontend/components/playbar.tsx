"use client";
import * as React from "react";
import { useCurrentSong, useIsPlaying } from "~/app/atoms";
import * as Icons from "~/components//icons";
import { Slider } from "~/components/slider";
import { API_URL } from "~/app/contants";
import { twMerge } from "tailwind-merge";

function useInterval(callback: (...args: any[]) => any, delay: number) {
  const savedCallback = React.useRef<(...args: any[]) => any>();
  const [callbackRunning, setCallbackRunning] = React.useState(true);

  React.useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  React.useEffect(() => {
    function tick() {
      callbackRunning && savedCallback.current?.();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);

  return setCallbackRunning;
}

export function Playbar() {
  const { song } = useCurrentSong();
  const audioTrack = React.useRef<HTMLAudioElement>(null);

  const [seekValue, setSeekValue] = React.useState<number | null>(null);
  const [progress, setProgress] = React.useState(0);
  const setIntervalRunning = useInterval(() => {
    if (!audioTrack.current) return;
    setProgress(audioTrack.current.currentTime);
  }, 100);

  const { isPlaying, setIsPlaying } = useIsPlaying();
  React.useEffect(() => {
    if (!audioTrack.current) return;
    if (isPlaying) {
      audioTrack.current.play();
    } else {
      audioTrack.current.pause();
    }
    setIsPlaying(isPlaying);
  }, [isPlaying]);

  function togglePlay() {
    if (audioTrack.current?.paused) {
      audioTrack.current?.play();
      setIsPlaying(true);
    } else {
      audioTrack.current?.pause();
      setIsPlaying(false);
    }
  }

  React.useEffect(() => {
    if (!song) return;
    if (audioTrack.current?.paused) audioTrack.current?.play();
    setIsPlaying(true);
  }, [song]);

  return (
    <div className="flex items-center justify-between h-full px-4">
      <div className="flex items-center gap-4 w-[64ch]">
        <img
          src={song?.cover_path}
          className="h-12 w-12 rounded-sm select-none"
        />
        <div className="flex flex-col">
          <h1 className="text-base font-bold">{song?.title}</h1>
          <h2 className="hover:underline cursor-pointer text-sm">
            {song?.artist_name}
          </h2>
        </div>
      </div>
      <audio ref={audioTrack} src={`${API_URL}${song?.mp3_path}`} />
      <Slider
        value={[seekValue ?? progress]}
        onValueChange={([value]) => {
          setIntervalRunning(false);
          setSeekValue(value);
        }}
        onValueCommit={([value]) => {
          setSeekValue(null);
          setProgress(value);
          setIntervalRunning(true);
          audioTrack.current!.currentTime = value!;
        }}
        max={audioTrack.current?.duration ?? 100}
        step={0.01}
      />
      <div className="flex items-center gap-4">
        <button className="rounded-full flex items-center justify-center w-10">
          <Icons.Previous className="h-4 w-4" />
        </button>
        <button
          className="rounded-full flex items-center justify-center w-10"
          onClick={togglePlay}
        >
          {isPlaying ? (
            <Icons.Pause className={twMerge("h-4 w-4")} />
          ) : (
            <Icons.Play className={twMerge("h-4 w-4")} />
          )}
        </button>
        <button className="rounded-full flex items-center justify-center w-10">
          <Icons.Next className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
