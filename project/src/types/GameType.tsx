export interface Game {
    name: string;
    scores: { [key: string]: number };
  }

export interface Games {
    date: string;
    games: Game[];
    players: string[];
  }