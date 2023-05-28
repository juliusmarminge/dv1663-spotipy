# Spotipy Backend

## Usage

1. Install deps

```bash
pip3 install -r requirements.txt
```

2. Start database

```sh
docker compose up -d
```

3. Initialize the database

```bash
python3 setup.py
python3 seed.py
```

3. Start server

```bash
uvicorn main:app --reload
```
