import React from "react";
import BjorliGame from "./containers/GamePage";
import { useDateState, useGamesState } from "./states/state";

function App() {
  const [date, dates, setDate] = useDateState();
  const [games] = useGamesState(date);

  return (
    <div>
      <select
        value={date}
        onChange={(event: React.ChangeEvent<HTMLSelectElement>) =>
          setDate(event.target.value)
        }
      >
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
