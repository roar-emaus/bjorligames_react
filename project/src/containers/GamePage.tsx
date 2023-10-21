import React from "react";
import "../App.css";
import AgGridTable from "../components/Table.tsx";
import { Games } from "../types/GameType.tsx";

type BjorliGameProps = {
  games: Games;
};

const BjorliGame: React.FC<BjorliGameProps> = ({ games }) => {
  // console.log(games);
  const columnDefs = [
    {
      headerName: "Deltager",
      field: "player", // This field should match the player name in rowData
    },
    ...games.games.map((game) => ({
      headerName: game.name,
      field: game.name,
      cellStyle: { textAlign: "right" }, // Right-align the text
      width: 100,
      autoHeaderHeight: true,
    })),
  ];

  const rowData = games.players.map((player) => {
    const playerData: Record<string, any> = { player };
    games.games.forEach((game) => {
      playerData[game.name] = game.scores[player];
    });
    return playerData;
  });

  return (
    <div style={{ height: "500px" }}>
      <h1>{games.date}</h1>
      <AgGridTable rowData={rowData} columnDefs={columnDefs} />
    </div>
  );
};

export default BjorliGame;
