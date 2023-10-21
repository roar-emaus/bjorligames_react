import React from "react";
import BjorliGame from "./containers/GamePage";
import { Games } from "./types/GameType";
import axios from "axios";

async function fetchGamesData(date: string): Promise<Games> {
  try {
    const response = await axios.get<Games>(
      `http://localhost:8000/?date=${date}`
    );
    // console.log(response);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error("Failed to fetch data from the API");
  }
}
async function fetchDates(): Promise<string[]> {
  try {
    const response = await axios.get<string[]>("http://localhost:8000/dates");
    // console.log(response);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error("Failed to fetch data from the API");
  }
}

function App() {
  const today = new Date().toISOString().split("T")[0];
  const [games, setGames] = React.useState<Games>({
    date: today,
    games: [{ name: "No Game", scores: { "No player": 1 } }],
    players: ["No player"],
  });
  const [date, setDate] = React.useState<string>(today);
  const [dates, setDates] = React.useState<string[]>([today]);
  React.useEffect(() => {
    async function getDates() {
      try {
        const dates = await fetchDates();
        setDates(dates);
        setDate(dates[0]);
        const games = await fetchGamesData(date);
        setGames(games);
      } catch (error) {
        console.log(error);
      }
    }
    getDates();
    return () => {
      setDates([today]);
    };
  }, []);

  React.useEffect(() => {
    async function getGames(date: string) {
      try {
        const data = await fetchGamesData(date);
        setGames(data);
      } catch (error) {
        console.error(error);
      }
    }

    getGames(date);
    return () => {
      setGames({
        date: today,
        games: [{ name: "No Game", scores: { "No player": 1 } }],
        players: ["No player"],
      });
    };
  }, [date]);

  const handleDateChange = (event: { target: { value: any } }) => {
    const selectedDate = event.target.value;
    setDate(selectedDate); // Update the date state with the selected value
  };
  return (
    <div>
      <select value={date} onChange={handleDateChange}>
        {dates.map((date, index) => (
          <option key={index} value={date}>
            {date}
          </option>
        ))}
      </select>
      <div>
        <BjorliGame games={games} />
      </div>
    </div>
  );
}

export default App;
