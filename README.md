# spotipy music player

# Quickstart

This project includes a [backend](./backend/README.md) and a [frontend](./frontend/README.md). Refer to the respective README for how to run the application. TL;DR

```bash
# in terminal 1
cd backend
pip3 install -r requirements.tsx

docker compose up -d

python3 setup.py
python3 seed.py

uvicorn main:app --reload

# in terminal 2
cd frontend
npm install
npm run dev
```

# Architecture

![arch](https://github.com/juliusmarminge/spotipy/assets/51714798/f37599a4-21d2-49c6-abcc-6b9953e20280)

# ER Diagram

![er](https://github.com/juliusmarminge/spotipy/assets/51714798/b818c673-4b0f-4f68-a915-3e8a8352dd38)

# SQL Tables

![tables](https://github.com/juliusmarminge/spotipy/assets/51714798/b95c6b07-0fb7-4ce9-9ac5-b4541127b42b)
