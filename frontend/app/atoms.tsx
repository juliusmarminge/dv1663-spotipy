import { atom, useAtom } from "jotai";

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
  const [song, _setSong] = useAtom(currentSongAtom);
  const [_1, setIsPlaying] = useAtom(isPlayingAtom);

  const setSong = (song: PlayingSong | null) => {
    if (!song) {
      setIsPlaying(false);
      _setSong(null);
      return;
    }
    setIsPlaying(true);
    _setSong(song);
  };

  return { song, setSong };
};
