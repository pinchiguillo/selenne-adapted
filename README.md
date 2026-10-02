# Selenne

Selenne is a Discord bot I wrote in Python as a personal project between 2022 and 2023.
It started as a small chat bot and grew into a modular bot built on
[discord.py](https://github.com/Rapptz/discord.py) 2.x: the core loads extensions (cogs) listed in a
YAML config file, keeps a MySQL connection open and registers slash commands.

**This is an archived personal project.** It is no longer maintained or deployed, several
extensions were never finished, and the code reflects what I knew at the time. This repository
holds the final state of version "Selenium 5.5b" (July 2023).

Before publishing, the repository was cleaned: credentials, logs, database dumps and other
people's data were removed from the whole history, and a few server-specific extensions were
dropped.

## What is in here

| Path | Contents |
| --- | --- |
| `main.py`, `Selenne.py` | Entry point and core: config loading, logging, MySQL connection, extension loading. |
| `extension/system/BotStats.py` | `/stats`: version, host node and server/user counts, plus release notes from `releases.json`. |
| `extension/AdminTools.py` | Moderation slash commands: timeout (`/isloate`), `/kick`, `/ban`, `/clear`. |
| `extension/essentials.py` | `/serverinfo`, `/whois` and `/echo`. |
| `extension/custom/DAM.py` | Unfinished viewer for my study notes from a programming course (DAM); notes live in `LDB/DAM/DAM1`. |
| `extension/teemplate.py` | Template used to start new extensions (`MusicPlayer.py` is still just a copy of it). |
| `old_extension/` | Extensions from earlier versions (XP levels, promo codes, a game item "forge", a guild/channel registry, ...). They are not loaded by default and not all of them work with the current core. |
| `tools/localdb_manager.py` | SQLite helper for a planned RPG-style profile system. |
| `LDB/` | Local data used by the extensions: study notes and game design prototypes. |

## Requirements

- Python 3.11
- The packages in `requeriments.txt` (`discord.py`, `PyYAML`, `mysql-connector-python`, `PyNaCl`)
- A MySQL server: the core connects to it on startup. There is no schema file; the extensions
  expect their tables (`guild`, `channel`, `leveling_xp`, `promocodes`, `blacksmith`) to exist.
- A Discord application with a bot token

## Configuration

1. Copy `config.example.yaml` to `config.yaml`. `config.yaml` is ignored by git.
2. Provide the secrets, preferably as environment variables instead of writing them in the file:
   - `SELENNE_TOKEN`: the Discord bot token
   - `SELENNE_OWNER_ID`: your Discord user ID (used for owner-only messages)
   - `SELENNE_DB_PASSWORD`: the MySQL password
3. Adjust the database host, user and name, and the `extensions` list, in `config.yaml`.
4. Optional: to give people access to the DAM notes, copy `LDB/DAM/users.example.json` to
   `LDB/DAM/users.json` (also ignored by git) and add their Discord user IDs.

## Running

On Windows, `install.bat` creates a virtual environment in `env/` and installs the requirements,
and `Selenne.bat` starts the bot. On any platform:

```sh
python -m venv env
source env/bin/activate          # Windows: env\Scripts\activate
pip install -r requeriments.txt
python main.py
```

Slash commands are not synced automatically: set `tree_sync = True` in `Selenne.py` to sync them
on startup.

## Known limitations

- `/kick` kicks the member who runs the command instead of taking a target.
- The DAM notes cog is not registered (`COGS` is empty in `extension/custom/DAM.py`).
- Most modules in `old_extension/` were written for older versions of the core and need changes
  before they can be loaded again.

## License

No license has been chosen for this repository yet.
