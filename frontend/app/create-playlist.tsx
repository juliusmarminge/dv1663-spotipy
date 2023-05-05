"use client";

const API_URL = "http://127.0.0.1:8000";

export function PlaylistForm() {
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        console.log(event);
        const fd = new FormData(event.currentTarget);
        const name = fd.get("name");

        console.log({ name });

        fetch(`${API_URL}/playlists?name=${name}`, {
          method: "POST",
          //   body: JSON.stringify({ name }),
        });
      }}
    >
      <input type="text" name="name" className="text-black" />
      <button type="submit">Create Playlist!</button>
    </form>
  );
}
