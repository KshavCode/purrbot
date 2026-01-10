# Discord Bot
A small Python project containing a bot-like application and data files used at runtime.

## Contents
- **Overview**: what the project is and which files are important
- **Quick Start**: create a venv, install dependencies, run `main.py`
- **Project structure**: short description of each top-level file and folders
- **Data & persistence**: how JSON data and `userdata/` are used
- **Security**: guidance about `secrets.json`

## Overview
This repository contains a Python-based bot-style application. The entry point is `main.py`. The project relies on JSON data files stored in `data/` and lightweight persistent user data stored in `userdata/`.

## Quick Start (Windows PowerShell)
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python main.py
```

If your environment prevents script execution, run PowerShell as administrator or adjust the execution policy (be mindful of security).

## Project Structure

- `main.py`: Application entry point.
- `FunctionFiles.py`: Shared functions and helpers used by `main.py`.
- `requirements.txt`: Python dependencies for the project.
- `secrets.json`: Configuration for secrets such as tokens or keys. DO NOT commit sensitive values.
- `feedback.txt`: Free-form feedback or notes.
- `data/`: JSON resources used by the bot.
  - `animals.json`, `animals_emoji.json`, `help.json`, `roleplay.json`, `shop.json` — example data resources used by the application.
- `userdata/`: runtime persistent data written by the app.
  - `hug_count.json`, `slap_count.json`, `inventory.json` — counters and per-user data.
  - `users.csv`: user records

## Data & Persistence
- The `data/` folder stores read-only resource files the app reads at runtime.
- The `userdata/` folder stores runtime-modified JSON files and should be writable by the running process.
- If you back up or reset data, copy or remove files in `userdata/` carefully to avoid loss.

## Configuration & Secrets

- `secrets.json` likely contains API keys, tokens, or other sensitive settings. Do not add secrets to version control. Use environment variables or a separate secure store for production deployments.

## Development Notes

- When adding new data files, place them in `data/` and update code in `FunctionFiles.py` or `main.py` as needed.
- Run `python -m pip install -r requirements.txt` after changing dependencies.

## Contributing
- Fork or branch, implement changes, and open a pull request with a clear description of your changes.

## Support
- For quick notes or issues, add them to `feedback.txt` or open an issue in your chosen tracker.
