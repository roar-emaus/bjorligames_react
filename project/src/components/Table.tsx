import React from "react";
import { AgGridReact } from "ag-grid-react";
import { ColDef } from "ag-grid-community";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

interface AgGridTableProps {
  rowData: any[];
  columnDefs: ColDef[];
}

const AgGridTable: React.FC<AgGridTableProps> = ({ rowData, columnDefs }) => {
  return (
    <div className="ag-theme-alpine">
      <AgGridReact
        rowData={rowData}
        columnDefs={columnDefs}
        gridOptions={{ domLayout: "print" }}
      />
    </div>
  );
};

export default AgGridTable;
