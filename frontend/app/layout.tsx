import "./globals.css";
import { Inter } from "next/font/google";
import { Playlists } from "~/components/playlist-list";
import * as Icons from "~/components/icons";
import { Playbar } from "~/components/playbar";
import { twMerge } from "tailwind-merge";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata = {
  title: "Spotipy",
  description: "A bad Spotify clone written in Python and React",
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={twMerge(inter.variable, "font-sans")}>
        <div className="container mx-auto relative h-screen">
          <h1 className="text-4xl font-bold pt-12 pb-6">Spotipy</h1>
          <div className="flex gap-4 h-[calc(100vh-12rem)]">
            <aside className="max-w-sm rounded-lg overflow-y-scroll space-y-4">
              <nav className="p-4 rounded-lg max-w-sm space-y-4 bg-background-muted">
                <ul className="flex flex-col gap-4 font-semibold text-lg">
                  <li className="flex items-center gap-4 hover:text-foreground-muted cursor-pointer">
                    <Icons.Home /> Home
                  </li>
                  <li className="flex items-center gap-4 hover:text-foreground-muted cursor-pointer">
                    <Icons.Search /> Search
                  </li>
                </ul>
              </nav>
              {/* @ts-expect-error */}
              <Playlists />
            </aside>
            <main className="bg-background-muted rounded-lg flex-1 overflow-y-scroll relative">
              {children}
            </main>
          </div>
          <footer className="absolute bottom-0 inset-x-0 h-16 bg-background-muted rounded-t-lg">
            <Playbar />
          </footer>
        </div>
      </body>
    </html>
  );
}
