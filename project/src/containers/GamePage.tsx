import React, { useMemo } from "react";
import "../App.css";
import AgGridTable from "../components/Table.tsx";
import { Games } from "../types/GameType.tsx";
import { GamesState } from "../states/state.tsx";

interface BjorliGameProps {
  games: GamesState["games"];
}

interface RowData {
  player: string;
  [key: string]: number | string;
}

interface ColumnDefinition {
  headerName: string;
  field?: string;
  valueGetter?: (params: any) => any;
  cellStyle?: object;
  width?: number;
  autoHeaderHeight?: boolean;
  sortable?: boolean;
  editable?: boolean;
  singleClickEdit?: boolean;
  cellEditor?: string;
  cellEditorParams?: object;
  cellDataType?: string;
}

function calculateTotalScore(games: Games, playerData: RowData): number {
  return games.games.reduce(
    (total, game) => total * (playerData[game.name] as number),
    1
  );
}

function getColumnDefinitions(games: Games): ColumnDefinition[] {
  const gameColumns = games.games.map((game) => ({
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
  }));

  return [
    { headerName: "Deltager", field: "player", sortable: true },
    ...gameColumns,
    {
      headerName: "Total",
      valueGetter: (params: any) => {
        return calculateTotalScore(games, params.data);
      },
      cellStyle: { textAlign: "right" },
      width: 100,
      autoHeaderHeight: true,
      sortable: true,
      cellDataType: "number",
    },
  ];
}

const BjorliGame: React.FC<BjorliGameProps> = ({ games }) => {
  const { date, players, games: gameData } = games;

  const columnDefs = useMemo(() => getColumnDefinitions(games), [games]);

  const rowData = useMemo(() => {
    return players.map((player) => {
      const playerData = gameData.reduce((data, game) => {
        data[game.name] = game.scores[player];
        return data;
      }, {} as Record<string, number>);

      return {
        player,
        ...playerData,
      };
    });
  }, [gameData, players]);

  return (
    <div style={{ height: "500px" }}>
      <h1>{date}</h1>
      <AgGridTable rowData={rowData} columnDefs={columnDefs} />
    </div>
  );
};

export default BjorliGame;
