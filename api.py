from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr, Field, conint, PositiveInt
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import csv
import os
import time

### TYPES

class Game(BaseModel):
    name: constr(min_length=2, max_length=50)  # Ensuring game name is between 2 to 50 characters
    scores: Dict[str, PositiveInt]  # Ensuring scores are positive integers

class BjorliGame(BaseModel):
    date: str = Field(..., description="Date in format YYYY-MM", pattern="^\d{4}-\d{2}$")
    locked: bool
    games: List[Game]
    players: List[constr(min_length=1, max_length=50)]  # Ensuring player names are between 1 to 50 characters

class DateQuery(BaseModel):
    date: str = Field(..., pattern="^\d{4}-\d{2}$")


### UTIL FUNCTIONS

def get_locked_games(data_path: Path) -> List[BjorliGame]:
    all_dates = []
    for file_path in get_all_game_paths(data_path):
        all_dates.append(csv_to_bjorligame(file_path))
    return all_dates


def get_newest_version_path(directory_path: Path) -> Optional[Path]:
    # Get all files that match the format {bjorli_game.date}_*.csv
    matching_files = list(directory_path.glob(f"*.csv"))
    # If no matching files, return None
    if not matching_files:
        return None
    # Identify the file with the largest UNIX timestamp
    newest_file = max(matching_files, key=lambda x: int(x.stem.split('_')[-1]))
    print(newest_file)
    return newest_file

def get_all_game_paths(data_path: Path) -> List[Path]:
    return [filename for filename in data_path.iterdir() if filename.match("*.csv")]


def csv_to_bjorligame(file_path: Path) -> BjorliGame:
    game_names, players_scores = parse_csv(file_path)
    date = extract_date_from_filename(file_path)
    games = construct_games(game_names, players_scores)
    locked = False
    
    if "locked" in str(file_path):
        locked = True
    print(date, locked)
    return BjorliGame(date=date, locked=locked, games=games, players=list(players_scores.keys()))

def parse_csv(file_path: Path) -> (List[str], Dict[str, List[int]]):
    print(file_path)
    with open(file_path, 'r') as score_file:
        csv_reader = csv.reader(score_file)
        
        game_names = next(csv_reader)[1:]
        
        players_scores = {}
        for row in csv_reader:
            player_name = row[0]
            scores = list(map(int, row[1:]))
            players_scores[player_name] = scores

    return game_names, players_scores

def extract_date_from_filename(file_path: Path) -> str:
    new_file_name = file_path.stem.replace('_', '-')
    if split_name := new_file_name.split('-'):
        return '-'.join(split_name[:2])
    return new_file_name

def construct_games(game_names: List[str], players_scores: Dict[str, List[int]]) -> List[Game]:
    games = []
    
    for game_index, game_name in enumerate(game_names):
        scores = {player: scores[game_index] for player, scores in players_scores.items()}
        games.append(Game(name=game_name, scores=scores))
    
    return games

def is_game_locked(date: str) -> bool:
    games = DATA_STORAGE['games'].get(date)
    if not games:
        return False
    latest_game = games[-1]
    latest_game_instance = BjorliGame.parse_raw(latest_game)
    return latest_game_instance.locked

def bjorligame_to_csv(bjorli_game: BjorliGame, save_path: Path):
    # Generate filename with the date and a UNIX timestamp
    filename = f"{bjorli_game.date.replace('-','_')}_{int(time.time())}.csv"
    file_path = save_path / filename

    # Construct CSV data
    header = ['Player'] + [game.name for game in bjorli_game.games]
    
    rows = []
    for player in bjorli_game.players:
        row = [player]
        for game in bjorli_game.games:
            row.append(game.scores.get(player, 0))  # Default score to 0 if not present
        rows.append(row)

    # Write to CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# This will store our in-memory data

DATA_STORAGE = {
    'dates': [],
    'games': {},
    'latest_date': None
}

@app.on_event("startup")
async def load_data_on_startup():
    locked_path = Path(os.environ.get("LOCKED_PATH", ""))
    all_locked_games = get_locked_games(locked_path)
    for game in all_locked_games:
        game_data = game.json()
        DATA_STORAGE['games'].setdefault(game.date, []).append(game_data)
        DATA_STORAGE['dates'].append(game.date)
        DATA_STORAGE['latest_date'] = game.date

    newest_file_path = get_newest_version_path(locked_path.parent)
    editable_bjorligame = csv_to_bjorligame(newest_file_path)
    game_data = editable_bjorligame.json()
    DATA_STORAGE['games'].setdefault(editable_bjorligame.date, []).append(game_data)
    DATA_STORAGE['dates'].append(editable_bjorligame.date)
    DATA_STORAGE['latest_date'] = editable_bjorligame.date


@app.get("/date/")
async def root() -> BjorliGame:
    return BjorliGame(
        date='2023-01',
        locked=False,
        games=[Game(name='No name', scores={'No name': 1})], players=['No name'])

@app.get("/date/{date}")
async def get_date_data(date: str) -> BjorliGame:
    try:
        validated_date = DateQuery(date=date)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    print(f"Called /date/{validated_date}")
    games = DATA_STORAGE['games'].get(validated_date.date)

    if not games:
        return BjorliGame(
            date='2023-01',
            locked=False,
            games=[Game(name='No name', scores={'No name': 1})], players=['No name'])
    latest_game = games[-1]
    return BjorliGame.parse_raw(latest_game)


@app.get("/dates")
async def get_dates() -> List[str]:
    all_dates = DATA_STORAGE['dates']
    print("Called /dates", all_dates)
    return sorted(list(set(date for date in all_dates)))[::-1]


@app.post("/game")
async def add_game(game: BjorliGame):
    print("Called /game", game.date)

    if is_game_locked(game.date):
        print("Cannot modify a locked game")
        raise HTTPException(status_code=400, detail="Cannot modify a locked game")
    game_data = game.model_dump_json()
    DATA_STORAGE['games'].setdefault(game.date, []).append(game_data)
    DATA_STORAGE['dates'].append(game.date)
    DATA_STORAGE['latest_date'] = game.date
    
    bjorligame_to_csv(game, Path(os.environ.get("LOCKED_PATH", "")).parent)  # Save to the same directory where the `locked` folder is

    return {"status": "success", "message": "Game modified successfully"}

@app.post("/lock/{date}")
async def lock_game(date: str):
    try:
        validated_date = DateQuery(date=date)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    games = DATA_STORAGE['games'].get(validated_date.date)
    if not games:
        raise HTTPException(status_code=404, detail="Game data not found for this date")
    
    latest_game = games[-1]
    latest_game_instance = BjorliGame.parse_raw(latest_game)
    latest_game_instance.locked = True
    games[-1] = latest_game_instance.json()  # Update the game as locked
    return {"status": "success", "message": "Game locked successfully"}


if __name__ == "__main__":
    import argparse
    import uvicorn
    
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="FastAPI App with Command-Line Arguments")
    parser.add_argument("--locked", default=None, help="The path of the locked scores")
    args = parser.parse_args()
    os.environ["LOCKED_PATH"] = args.locked
    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)
