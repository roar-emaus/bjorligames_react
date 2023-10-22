from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path


class Game(BaseModel):
    name: str
    scores: Dict[str, int]


class Games(BaseModel):
    date: str
    games: List[Game]
    players: List[str]


def start_up():
    data_folder = Path('/bjorligames/data')
    games = []
    for game_folder in data_folder.iterdir():
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


games = start_up()

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

@app.get("/date/")
async def root() -> Games:
    return Games(
        date='',
        games=[Game(name='No name', scores={'No name': 0})], players=['No name'])

@app.get("/date/{date}")
async def root(date: str) -> Games:
    print(f"Called /date/{date}")
    for bjorligame in games:
        if date == bjorligame.date:
            return bjorligame
    return Games(
        date='',
        games=[Game(name='No name', scores={'No name': 0})], players=['No name'])


@app.get("/dates")
async def get_dates() -> List[str]:
    print("Called /dates: ", [g.date for g in games])
    return sorted([g.date for g in games])