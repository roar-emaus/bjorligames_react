import { useState, useEffect } from "react";
import { Games } from "../types/GameType";
import { fetchDates, fetchGamesData } from "../api/api";

export function useDateState(): [string, string[], (date: string) => void] {
  const [date, setDate] = useState("");
  const [dates, setDates] = useState<string[]>([]);

  const handleDateChange = (selectedDate: string) => {
    setDate(selectedDate);
  };

  async function getDates() {
    try {
      const dates = await fetchDates();
      setDates(dates);
    } catch (error) {
      console.error(error);
    }
  }
  useEffect(() => {
    getDates();
  }, []);

  return [date, dates, handleDateChange];
}

export function useGamesState(date: string): [Games] {
  const initialGamesState: Games = {
    date: "",
    games: [{ name: "No Game", scores: { "No player": 1 } }],
    players: ["No player"],
  };

  const [games, setGames] = useState(initialGamesState);

  useEffect(() => {
    async function getGames() {
      try {
        const gamesData = await fetchGamesData(date);
        setGames(gamesData);
      } catch (error) {
        console.error(error);
      }
    }

    getGames();
  }, [date]);

  return [games];
}
