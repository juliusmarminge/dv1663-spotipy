"use client";

import * as React from "react";
import { Input } from "~/ui/input";
import * as Icons from "~/ui/icons";
import { useRouter } from "next/navigation";

export function SearchBox() {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState("");

  const router = useRouter();

  if (!open)
    return (
      <li
        className="flex items-center gap-4 hover:text-foreground-muted cursor-pointer"
        onClick={() => setOpen(true)}
      >
        <Icons.Search /> Search
      </li>
    );

  return (
    <form
      onSubmit={() => {
        setOpen(false);
        setSearch("");
        router.push(`/songs?search=${search.trim()}`);
      }}
    >
      <Input
        placeholder="Search"
        value={search}
        autoFocus
        onChange={(e) => setSearch(e.target.value)}
        onFocus={() => setOpen(true)}
        onBlur={() => setOpen(false)}
        className="w-full"
      />
    </form>
  );
}
