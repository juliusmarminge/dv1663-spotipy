# spotipy music player

# Quickstart

This project includes a [backend](./backend) and a [frontend](./frontend). Refer to the respective README for how to run the application. TL;DR

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

![arch](https://github.com/juliusmarminge/spotipy/assets/51714798/70b39bd2-3d3b-44bd-8494-3c5e70fb2f27)

# ER Diagram

![image](https://github.com/juliusmarminge/dv1663-spotipy/assets/51714798/34b1cfa5-9343-4cdb-a278-fe1dbe25a0a3)

# SQL Tables

![tables](https://github.com/juliusmarminge/spotipy/assets/51714798/bdc29afc-9108-49c2-aaa8-a20ce75670ac)

