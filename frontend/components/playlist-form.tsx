"use client";

import { useRouter } from "next/navigation";
import * as React from "react";
import { API_URL } from "~/app/contants";
import { Button } from "~/components/button";
import { Input } from "~/components/input";

export function CreatePlaylistForm(props: { user?: string }) {
  const ref = React.useRef<HTMLFormElement>(null);
  const router = useRouter();

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const fd = new FormData(event.currentTarget);
    const name = fd.get("name");

    if (!name) return alert("Please enter a name");

    await fetch(`${API_URL}/playlists`, {
      method: "POST",
      body: JSON.stringify({ name }),
      headers: {
        "Content-Type": "application/json",
        ...(props.user ? { Authorization: props.user } : {}),
      },
    });

    ref.current?.reset();
    router.refresh();
  }

  return (
    <form
      ref={ref}
      className="flex gap-2 w-full max-w-lg"
      onSubmit={handleSubmit}
    >
      <Input type="text" name="name" placeholder="Playlist Name" />
      <Button type="submit">Create</Button>
    </form>
  );
}
