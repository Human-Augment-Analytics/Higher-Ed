import { useState } from "react";
import tableData1 from "../tableData1.json";
import TableBody from "./TableBody";
import TableHead from "./TableHead";
import { useSortableTable } from "../useSortableTable";

const Table = ({ caption, data, columns }) => {
    const [tableData, handleSorting] = useSortableTable(data, columns);
  
    return (
      <>
        <table className="table">
          <caption>{caption}</caption>
          <TableHead {...{ columns, handleSorting }} />
          <TableBody {...{ columns, tableData }} />
        </table>
      </>
    );
};

export default Table;