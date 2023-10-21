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
      field: "player",
      sortable: true,
    },
    ...games.games.map((game) => ({
      headerName: game.name,
      field: game.name,
      cellStyle: { textAlign: "right" },
      width: 100,
      autoHeaderHeight: true,
      sortable: true,
      editable: true,
      singleClickEdit: true,
      cellEditor: "agNumberCellEditor",
      cellEditorParams: {
        min: 1,
        max: games.players.length,
        precision: 0,
      },
      cellDataType: "number",
    })),
    {
      headerName: "Total",
      valueGetter: (params: any) => {
        let total = 1;
        games.games.forEach((game) => {
          total *= params.data[game.name];
        });
        return total;
      },
      cellStyle: { textAlign: "right" },
      width: 100,
      autoHeaderHeight: true,
      sortable: true,
      cellDataType: "number",
    },
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
