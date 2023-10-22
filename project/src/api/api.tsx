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
