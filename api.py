from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import redis

class Game(BaseModel):
    name: str
    scores: Dict[str, int]


class Games(BaseModel):
    date: str
    games: List[Game]
    players: List[str]


def start_up():
    data_folder = Path('/workspaces/bjorligame/data')
    games = []
    for game_folder in data_folder.iterdir():
        if game_folder.is_dir():
            with open(game_folder/'poeng.csv') as score_file:
                game_names = score_file.readline().strip().split(',')[1:]
                date = game_folder.name.replace('_','-')
                
                players = {}
                for player in score_file.readlines():
                    player_scores = player.strip().split(',')
                    players[player_scores[0]] = list(map(int ,player_scores[1:]))
                this_bjorligame = []
                for game_index, game_name in enumerate(game_names):
                    this_bjorligame.append(
                        Game(name=game_name, scores={pn: s[game_index] for pn, s in players.items()})
                    )
            games.append(Games(date=date, games=this_bjorligame, players=list(players.keys())))
    return games


# games = start_up()

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

# @app.get("/date/")
# async def root() -> Games:
#     return Games(
#         date='',
#         games=[Game(name='No name', scores={'No name': 0})], players=['No name'])

# @app.get("/date/{date}")
# async def root(date: str) -> Games:
#     print(f"Called /date/{date}")
#     for bjorligame in games:
#         if date == bjorligame.date:
#             return bjorligame
#     return Games(
#         date='',
#         games=[Game(name='No name', scores={'No name': 0})], players=['No name'])


# @app.get("/dates")
# async def get_dates() -> List[str]:
#     print("Called /dates: ", [g.date for g in games])
#     return sorted([g.date for g in games])

# @app.post("/game")
# async def add_game(game: Games) -> Games:
#     print("Called /game", game)
#     # games.append(game)
#     return game


redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/date/")
async def root() -> Games:
    return Games(
        date='',
        games=[Game(name='No name', scores={'No name': 0})], players=['No name'])

@app.get("/date/{date}")
async def root(date: str) -> Games:
    print(f"Called /date/{date}")
    games = redis_client.lrange(date, 0, -1)
    if not games:
        return Games(
            date='',
            games=[Game(name='No name', scores={'No name': 0})], players=['No name'])
    latest_game = games[-1].decode('utf-8')
    return Games.model_validate_json(latest_game)


@app.get("/dates")
async def get_dates() -> List[str]:
    all_dates = redis_client.lrange('dates', 0, -1)
    print("Called /dates", all_dates)
    return list(set(date.decode('utf-8') for date in all_dates))


@app.post("/game")
async def add_game(game: Games) -> Games:
    print("Called /game", game)
    timestamp = redis_client.time()[0]
    game_data = game.model_dump_json()
    redis_client.rpush(game.date, game_data)
    redis_client.zadd(game.date + '_timestamps', {game_data: timestamp})
    redis_client.lpush('dates', game.date)
    redis_client.set('latest_date', game.date)
    redis_client.save()
    return game