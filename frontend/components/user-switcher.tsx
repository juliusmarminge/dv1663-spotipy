"use client";

import * as React from "react";
import { Button } from "./button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./dropdown-menu";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./dialog";
import { Input } from "./input";

const imaginaryUsers = [
  {
    id: 1,
    username: "johndoe",
    avatar:
      "https://fastly.picsum.photos/id/868/200/200.jpg?hmac=TH6VPbfiRO1pMY4ZYWqECwlH8wSnlxN_KlCVOzTpbe8",
  },
  {
    id: 2,
    username: "janedoe",
    avatar:
      "https://fastly.picsum.photos/id/26/200/200.jpg?hmac=A1fbIskzMWVQs1JuyIsJXYGuCgqVwevLXT4YaIJM3Rk",
  },
  {
    id: 3,
    username: "jimdoe",
    avatar:
      "https://fastly.picsum.photos/id/669/200/200.jpg?hmac=lAa_bMRK0BRBCTEvl1acVqTfEDrXQc0yNwi683-13cE",
  },
];
type User = (typeof imaginaryUsers)[number];

export function UserSwitcher() {
  const [ddOpen, setDdOpen] = React.useState(false);
  const [signInAs, setSignInAs] = React.useState<User | null>(null);
  const [user, setUser] = React.useState(imaginaryUsers[0]);

  function handleSignIn(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!signInAs) return;

    // TODO: validate password
    // TODO: persist active user in LS or Cookie
    setUser(signInAs);
    setSignInAs(null);
  }

  return (
    <Dialog
      open={!!signInAs}
      onOpenChange={(open) => !open && setSignInAs(null)}
    >
      <DropdownMenu open={ddOpen} onOpenChange={setDdOpen}>
        <DropdownMenuTrigger asChild>
          <Button className="p-0 h-10 w-10 rounded-full">
            <img src={user.avatar} className="rounded-full" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56" align="end">
          <DropdownMenuLabel className="font-semibold">
            Signed in as: {user.username}
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuLabel className="font-light text-sm text-foreground/80">
            Select user
          </DropdownMenuLabel>
          {imaginaryUsers
            .filter((u) => u.id !== user.id)
            .map((user) => (
              <DialogTrigger asChild>
                <DropdownMenuItem
                  key={user.id}
                  onClick={() => {
                    setDdOpen(false);
                    setSignInAs(user);
                  }}
                >
                  <span>{user.username}</span>
                </DropdownMenuItem>
              </DialogTrigger>
            ))}
        </DropdownMenuContent>
      </DropdownMenu>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Switch user</DialogTitle>
          <DialogDescription>
            <form onSubmit={handleSignIn} className="flex flex-col gap-4 mt-4">
              <Input placeholder="Password" type="password" />
              <Button type="submit">Sign in as {signInAs?.username}</Button>
            </form>
          </DialogDescription>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
}
