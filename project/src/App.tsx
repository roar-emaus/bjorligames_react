import React from "react";
import BjorliGame from "./containers/GamePage";
import { useDateState, useGamesState } from "./states/state";

function App() {
  const [dateState, setDateState] = useDateState();
  const [gamesState] = useGamesState(dateState.date);
  return (
    <div>
      <select
        value={dateState.date}
        onChange={(event: React.ChangeEvent<HTMLSelectElement>) =>
          setDateState(event.target.value)
        }
      >
        {dateState.dates.map((date, index) => (
          <option key={index} value={date}>
            {date}
          </option>
        ))}
      </select>
      <div>
        <BjorliGame games={gamesState.games} />
      </div>
    </div>
  );
}

export default App;
