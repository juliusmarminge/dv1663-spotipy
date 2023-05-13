import "./globals.css";
import { Inter } from "next/font/google";
import { Playlists } from "~/components/playlist-list";
import * as Icons from "~/components/icons";
import { Playbar } from "~/components/playbar";

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
      <body
        className={`${inter.variable} font-sans container mx-auto max-w-screen-xl h-screen relative`}
      >
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
          <main className="bg-background-muted rounded-lg flex-1 overflow-y-scroll">
            {children}
          </main>
        </div>
        <footer className="absolute bottom-0 w-full h-16 bg-background-muted rounded-t-lg">
          <Playbar />
        </footer>
      </body>
    </html>
  );
}
