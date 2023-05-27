import { atom, useAtom } from "jotai";
import { API_URL } from "./contants";

type PlayingSong = {
  id: number;
  title: string;
  artist_name: string;
  cover_path: string;
  mp3_path: string;
};

const currentSongAtom = atom<PlayingSong | null>(null);
const isPlayingAtom = atom(false);

export const useIsPlaying = () => {
  const [isPlaying, setIsPlaying] = useAtom(isPlayingAtom);
  return { isPlaying, setIsPlaying };
};

export const useCurrentSong = () => {
  const [currentSong, _setSong] = useAtom(currentSongAtom);
  const [_, setIsPlaying] = useAtom(isPlayingAtom);

  const setSong = (song: PlayingSong | null) => {
    if (!song) {
      setIsPlaying(false);
      _setSong(null);
      return;
    }

    setIsPlaying(true);
    _setSong(song);

    if (song.id !== currentSong?.id) {
      // register song played to backend - we're not doing some sophisticated
      // algorithm to determine how much of the song was played, we're just
      // registering that the song was played at all. this could use some improvement.
      fetch(`${API_URL}/song/${song.id}`, {
        method: "PUT",
      });
    }
  };

  return { song: currentSong, setSong };
};
