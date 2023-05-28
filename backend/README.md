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

If you prefer a different MySQL server, make sure the credentials are matched in [the configuration object](./setup.py):

```python
config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "password",
}
```

3. Initialize the database. The following script will initialize the database with the all the tables, triggers, procedures etc, as well as seeding it with some default data.

```bash
python3 setup.py
python3 seed.py
```

3. Start server

```bash
uvicorn main:app --reload
```
