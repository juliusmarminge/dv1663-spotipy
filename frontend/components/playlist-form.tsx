"use client";

import * as React from "react";
import { API_URL } from "~/app/contants";
import { Button } from "~/components/button";
import { Input } from "~/components/input";

export function CreatePlaylistForm() {
  const ref = React.useRef<HTMLFormElement>(null);
  return (
    <form
      ref={ref}
      className="flex gap-2 w-full max-w-lg"
      onSubmit={async (event) => {
        event.preventDefault();

        const fd = new FormData(event.currentTarget);
        const name = fd.get("name");

        await fetch(`${API_URL}/playlists`, {
          method: "POST",
          body: JSON.stringify({ name, user_id: 5 }),
          headers: {
            "Content-Type": "application/json",
          },
        });

        ref.current?.reset();
      }}
    >
      <Input type="text" name="name" placeholder="Playlist Name" />
      <Button type="submit">Create</Button>
    </form>
  );
}
