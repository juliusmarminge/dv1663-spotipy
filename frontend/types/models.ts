export interface Artist {
  id: number;
  name: string;
  biography: string;
}

export interface Song {
  id: number;
  title: string;
  artist_id: string;
  mp3_path: string;
  cover_path: string;
}

export interface User {
  id: number;
  username: string;
  password: string;
}

export interface Playlist {
  id: number;
  name: string;
  user_id: number;
}
