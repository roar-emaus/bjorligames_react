import { useState, useEffect } from "react";
import { Games } from "../types/GameType";
import { fetchDates, fetchGamesData } from "../api/api";

export interface DateState {
  date: string;
  dates: string[];
}

export interface GamesState {
  games: Games;
}

export function useDateState(): [DateState, (date: string) => void] {
  const [state, setState] = useState<DateState>({ date: "", dates: [] });

  const handleDateChange = (selectedDate: string) => {
    setState((prevState) => ({ ...prevState, date: selectedDate }));
  };

  async function getDates() {
    try {
      const dates = await fetchDates();
      setState((prevState) => ({ ...prevState, dates }));
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    getDates();
  }, []);

  return [state, handleDateChange];
}

export function useGamesState(date: string): [GamesState] {
  const initialGamesState: GamesState = {
    games: {
      date: "",
      games: [{ name: "No Game", scores: { "No player": 1 } }],
      players: ["No player"],
    },
  };

  const [state, setState] = useState<GamesState>(initialGamesState);

  useEffect(() => {
    async function getGames() {
      try {
        const gamesData = await fetchGamesData(date);
        setState((prevState) => ({ ...prevState, games: gamesData }));
      } catch (error) {
        console.error(error);
      }
    }

    getGames();
  }, [date]);

  return [state];
}
