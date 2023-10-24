from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import redis

### TYPES
class Game(BaseModel):
    name: str
    scores: Dict[str, int]


class BjorliGame(BaseModel):
    date: str
    locked: bool
    games: List[Game]
    players: List[str]


### UTIL FUNCTIONS

def get_locked_games(data_path: Path) -> List[BjorliGame]:
    all_dates = []
    for file_path in get_all_game_paths(data_path):
        all_dates.append(csv_to_bjorligame(file_path))
    return all_dates


def get_all_game_paths(data_path: Path) -> List[Path]:
    return [filename for filename in data_path.iterdir() if filename.match("*.csv")]


def csv_to_bjorligame(file_path: Path) -> BjorliGame:
    with open(file_path) as score_file:
        game_names = score_file.readline().strip().split(',')[1:]
        date = file_path.name.strip(".csv").replace('_','-')
                        
        players = {}
        for player in score_file.readlines():
            player_scores = player.strip().split(',')
            players[player_scores[0]] = list(map(int ,player_scores[1:]))
        games = []
        for game_index, game_name in enumerate(game_names):
            games.append(
                Game(name=game_name, scores={pn: s[game_index] for pn, s in players.items()})
            )
    return BjorliGame(date=date, locked=True, games=games, players=list(players.keys()))


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

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/date/")
async def root() -> BjorliGame:
    return BjorliGame(
        date='',
        locked=False,
        games=[Game(name='No name', scores={'No name': 0})], players=['No name'])

@app.get("/date/{date}")
async def root(date: str) -> BjorliGame:
    print(f"Called /date/{date}")
    games = redis_client.lrange(date, 0, -1)
    print(games)
    if not games:
        return BjorliGame(
            date='',
            locked=False,
            games=[Game(name='No name', scores={'No name': 0})], players=['No name'])
    latest_game = games[-1].decode('utf-8')
    return BjorliGame.model_validate_json(latest_game)


@app.get("/dates")
async def get_dates() -> List[str]:
    all_dates = redis_client.lrange('dates', 0, -1)
    print("Called /dates", all_dates)
    return list(set(date.decode('utf-8') for date in all_dates))


@app.post("/game")
async def add_game(game: BjorliGame) -> BjorliGame:
    print("Called /game", game)
    timestamp = redis_client.time()[0]
    game_data = game.model_dump_json()
    redis_client.rpush(game.date, game_data)
    redis_client.zadd(game.date + '_timestamps', {game_data: timestamp})
    redis_client.lpush('dates', game.date)
    redis_client.set('latest_date', game.date)
    redis_client.save()
    return game


def add_locked_game_to_redis(game: BjorliGame):
    game_data = game.model_dump_json()
    add_game_to_redis(game.date, game_data)
    redis_client.xadd(game.date + '_locked', {game_data: 'locked'})


def add_game_to_redis(date, game_data):
    redis_client.rpush(date, game_data)
    redis_client.lpush('dates', date)
    

if __name__ == "__main__":
    import argparse
    import uvicorn
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="FastAPI App with Command-Line Arguments")

    # Add the arguments you need
    parser.add_argument("--locked", default=None, help="The path of the locked scores")

    # Parse the command-line arguments
    args = parser.parse_args()
    locked_path = Path(args.locked)
    all_locked_games = get_locked_games(locked_path)
    for game in all_locked_games:
        add_locked_game_to_redis(game)

    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)
