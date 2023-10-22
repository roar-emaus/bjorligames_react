import axios from "axios";
import { Games } from "../types/GameType";

export async function fetchGamesData(date: string): Promise<Games> {
  try {
    const response = await axios.get<Games>(
      `http://localhost:8000/date/${date}`
    );
    console.log("fetchGamesData: ", response);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error("Failed to fetch data from the API");
  }
}

export async function fetchDates(): Promise<string[]> {
  try {
    const response = await axios.get<string[]>("http://localhost:8000/dates");
    console.log("fetchDates: ", response);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error("Failed to fetch data from the API");
  }
}

export async function onSendData(data: any[]) {
  const [year, month] = new Date().toISOString().split("-");
  const games: Games = {
    date: `${year}-${month}`,
    players: [],
    games: [],
  };

  // Extract the player names from the rowData
  const playerNames = new Set<string>();
  data.forEach((row) => {
    playerNames.add(row.player);
  });
  games.players = Array.from(playerNames);

  // Extract the game names and scores from the rowData
  const gameNames = new Set<string>();
  data.forEach((row) => {
    Object.keys(row).forEach((key) => {
      if (key !== "player") {
        gameNames.add(key);
      }
    });
  });
  games.games = Array.from(gameNames).map((name) => ({
    name,
    scores: {},
  }));

  data.forEach((row) => {
    const playerName = row.player;
    games.games.forEach((game) => {
      const score = row[game.name];
      game.scores[playerName] = score;
    });
  });

  try {
    const response = await axios.post("http://localhost:8000/game", games, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("onSendData: ", response);
    // Handle the successful response here
  } catch (error) {
    console.error(error);
    // Handle the error here, for example by displaying an error message to the user
  }
}
