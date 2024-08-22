import logo from './logo.svg';
import React, { useEffect } from 'react';
import './App.css';
import Table from "./components/Table";
import tableData1 from "./tableData1.json";

const columns = [
  // { label: "GTID", accessor: "gtid", sortable: false },
  { label: "Months Previously Volunteered", accessor: "months_previously_volunteered", sortable: true },
  { label: "Number of Months Interested", accessor: "num_months_interested", sortable: true },
  { label: "Has Research Experience", accessor: "has_research_xp", sortable: true },
  { label: "Has Previously Applied", accessor: "has_previously_applied", sortable: true },
  { label: "Is Potential Volunteer", accessor: "is_potential_volunteer", sortable: true },
  { label: "Has Used PACE", accessor: "has_used_pace", sortable: true },
  { label: "Has GPU", accessor: "has_gpu", sortable: true },
  { label: "GPU Type", accessor: "gpu_type", sortable: false },
  { label: "Classes Taken", accessor: "classes_taken", sortable: false },
  { label: "Programming Languages", accessor: "programming_languages", sortable: false },
  { label: "Email", accessor: "email", sortable: false }
];

const App = () => {
  return (
    <div className="app_header">
      <h1 className="header_text">HAAG Student Volunteer Resource Management</h1>
      <div className="table_container">
        <Table
          // caption="Developers currently enrolled in this course. The table below is ordered (descending) by the Gender column."
          data={tableData1}
          columns={columns}
        />
        <br />
      </div>
    </div>
  );
};

/*
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}
*/

export default App;
