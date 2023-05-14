"use client";

import * as React from "react";
import * as Icons from "./icons";
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
import { API_URL, LS_COOKIE_NAME } from "~/app/contants";
import { User } from "~/types/models";
import Image from "next/image";
import { useRouter } from "next/navigation";

// We don't persist avatars for users, so we'll just use a random one
const AVATAR = "https://i.pravatar.cc/100";

export function UserSwitcher() {
  const [dropdownOpen, setDropdownOpen] = React.useState(false);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [activeUser, setActiveUser] = React.useState<User | null>(null);
  const router = useRouter();

  async function fetchUser() {
    const user = localStorage.getItem(LS_COOKIE_NAME);
    if (!user) return;

    // check if the user is still valid
    const res = await fetch(API_URL + "/users/signin", {
      method: "POST",
      body: user,
      headers: { "Content-Type": "application/json" },
    });
    const json = await res.json();

    if (res.ok) {
      setActiveUser(json.user);
      document.cookie = `${LS_COOKIE_NAME}=${JSON.stringify(
        json.user
      )}; path=/;`;
      router.refresh();
    } else {
      // user had key in localstorage but the server rejected it
      localStorage.removeItem(LS_COOKIE_NAME);
      setActiveUser(null);
      alert("Your session has expired. Please sign in again.");
    }
  }

  React.useEffect(() => {
    // Fetch user on mount
    fetchUser();

    // Setup listerner for changes to localstorage
    function storageListener(e: StorageEvent) {
      if (e.key === LS_COOKIE_NAME) fetchUser();
    }

    window.addEventListener("storage", storageListener);
    return () => window.removeEventListener("storage", storageListener);
  }, []);

  return (
    <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
      <DropdownMenu open={dropdownOpen} onOpenChange={setDropdownOpen}>
        <DropdownMenuTrigger asChild>
          <Button className="p-0 h-10 w-10 rounded-full bg-background hover:bg-background-muted text-foreground">
            {activeUser ? (
              <Image
                src={AVATAR}
                className="rounded-full"
                height={100}
                width={100}
                priority
                alt="profile"
              />
            ) : (
              <Icons.User />
            )}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56" align="end">
          {activeUser && (
            <>
              <DropdownMenuLabel className="font-semibold">
                Hello {activeUser?.username}
              </DropdownMenuLabel>
              <DropdownMenuSeparator />

              <DropdownMenuItem
                onClick={() => {
                  setActiveUser(null);
                  localStorage.removeItem(LS_COOKIE_NAME);
                  document.cookie = `${LS_COOKIE_NAME}=; path=/;`;
                  router.refresh();
                }}
                className="flex justify-between cursor-pointer"
              >
                <span>Sign out</span>
                <Icons.SignOut className="text-foreground/70 h-4" />
              </DropdownMenuItem>
            </>
          )}

          {!activeUser && (
            <DialogTrigger asChild>
              <DropdownMenuItem
                onClick={() => {
                  setDropdownOpen(false);
                  setDialogOpen(true);
                }}
                className="flex justify-between cursor-pointer"
              >
                <span>Sign In</span>
                <Icons.SignIn />
              </DropdownMenuItem>
            </DialogTrigger>
          )}
        </DropdownMenuContent>
      </DropdownMenu>

      <SignInDialog onSubmitDone={() => setDialogOpen(false)} />
    </Dialog>
  );
}

function SignInDialog(props: { onSubmitDone: () => void }) {
  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    // @ts-expect-error - TS doesn't know about submitter ???
    const isSignUp = e.nativeEvent.submitter.value === "sign-up";
    const endpoint = isSignUp ? "/users/signup" : "/users/signin";

    const res = await fetch(API_URL + endpoint, {
      method: "POST",
      body: JSON.stringify({
        username: formData.get("username"),
        password: formData.get("password"), // should be hashed, whatever
      }),
      headers: { "Content-Type": "application/json" },
    });
    const json = await res.json();
    if (!res.ok) return alert(json.message);

    // update and send event to trigger eventlisteners
    window.localStorage.setItem(LS_COOKIE_NAME, JSON.stringify(json.user));
    window.dispatchEvent(new StorageEvent("storage", { key: LS_COOKIE_NAME }));

    // close dialog
    props.onSubmitDone();
  }

  return (
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Sign in as</DialogTitle>
        <DialogDescription>Enter user credentials</DialogDescription>
        <div className="pt-2">
          <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <Input placeholder="Username" type="text" name="username" />
            <Input placeholder="Password" type="password" name="password" />
            <Button type="submit" value="sign-in">
              Sign in
            </Button>
            <Button
              type="submit"
              value="sign-up"
              className="bg-transparent text-foreground hover:bg-transparent/80"
            >
              Don't have an account? Sign up
            </Button>
          </form>
        </div>
      </DialogHeader>
    </DialogContent>
  );
}
