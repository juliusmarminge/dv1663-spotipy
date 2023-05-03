from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/songs")
async def songs():
    # TODO: get songs from db
    songs = [
        {
            "id": 1,
            "title": "Danger Zone",
            "artist": "Harold Faltermeyer",
            "mp3_path": "/songs/song1.mp3",
            "cover_path": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
        },
        {
            "id": 2,
            "title": "Great Balls of Fire",
            "artist": "Miles Teller",
            "mp3_path": "/songs/song2.mp3",
            "cover_path": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2128&q=80",
        },
        {
            "id": 3,
            "title": "I Ain't Worried",
            "artist": "One Republic",
            "mp3_path": "/songs/song3.mp3",
            "cover_path": "https://images.unsplash.com/photo-1563089145-599997674d42?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
        },
    ]
    return songs
