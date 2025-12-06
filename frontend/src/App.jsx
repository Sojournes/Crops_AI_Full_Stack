import React, { useState } from "react";
import Chat from "./components/Chat";
import Visualizations from "./components/Visualizations";

function App() {
  const [plotData, setPlotData] = useState(null);

  return (
    <div className="container">
      <Chat setPlotData={setPlotData} />
      <Visualizations data={plotData} />
    </div>
  );
}

export default App;
