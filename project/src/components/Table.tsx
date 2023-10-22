import React from "react";
import { AgGridReact } from "@ag-grid-community/react";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { ModuleRegistry } from "@ag-grid-community/core";
import { ClientSideRowModelModule } from "@ag-grid-community/client-side-row-model";

ModuleRegistry.registerModules([ClientSideRowModelModule]);

interface AgGridTableProps {
  rowData: any[];
  columnDefs: any[];
}

const AgGridTable: React.FC<AgGridTableProps> = ({ rowData, columnDefs }) => {
  return (
    <div className="ag-theme-alpine" style={{ height: "100%", width: "100%" }}>
      <AgGridReact rowData={rowData} columnDefs={columnDefs} />
    </div>
  );
};

export default AgGridTable;
