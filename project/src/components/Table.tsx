import React from "react";
import { AgGridReact } from "@ag-grid-community/react";
import { ModuleRegistry } from "@ag-grid-community/core";
import { ClientSideRowModelModule } from "@ag-grid-community/client-side-row-model";
import { onSendData } from "../api/api";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

ModuleRegistry.registerModules([ClientSideRowModelModule]);

interface AgGridTableProps {
  rowData: any[];
  columnDefs: any[];
}

const AgGridTable: React.FC<AgGridTableProps> = React.memo(
  ({ rowData, columnDefs }) => {
    const gridOptions = {};

    const handleSendData = () => {
      onSendData(rowData);
    };

    return (
      <div
        className="ag-theme-alpine"
        style={{ height: "100%", width: "100%" }}
      >
        {" "}
        <div style={{ marginBottom: "10px" }}>
          <button onClick={handleSendData}>Send Data</button>
        </div>
        <AgGridReact
          rowData={rowData}
          columnDefs={columnDefs}
          gridOptions={gridOptions}
        />
      </div>
    );
  }
);

export default AgGridTable;
