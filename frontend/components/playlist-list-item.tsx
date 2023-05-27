"use client";

import * as React from "react";
import * as Icons from "~/components/icons";
import { Button } from "~/components/button";
import { Playlist } from "~/types/models";
import { API_URL, LS_COOKIE_NAME } from "~/lib/contants";
import Link from "next/link";
import { useRouter } from "next/navigation";

export function PlaylistListItem(props: { playlist: Playlist }) {
  const router = useRouter();
  const [deleting, startTransition] = React.useTransition();

  async function handleDelete() {
    const user = localStorage.getItem(LS_COOKIE_NAME);
    const res = await fetch(`${API_URL}/playlists/${props.playlist.id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        ...(user ? { Authorization: user } : {}),
      },
    });

    const json = await res.json();
    console.log(json);
    if (!res.ok) {
      alert(json.message);
      return;
    }

    router.push("/");
    router.refresh();
  }

  return (
    <Link
      href={`/playlist/${props.playlist.id}`}
      className="hover:bg-background p-2 rounded flex justify-between items-center group"
    >
      <span>{props.playlist.name}</span>
      <Button
        className="bg-transparent text-foreground p-0 h-max hover:bg-transparent/70 invisible group-hover:visible"
        onClick={handleDelete}
      >
        <Icons.Trash className="h-4" />
      </Button>
    </Link>
  );
}
