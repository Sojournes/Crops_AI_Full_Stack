import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const data = [
  { name: "Corn", price: 257, demand: 200 },
  { name: "Soybean", price: 141, demand: 180 },
  { name: "Wheat", price: 130, demand: 150 },
  { name: "Rice", price: 180, demand: 196 },
];

export default function Visualizations() {
  return (
    <div className="card viz-container">
      <h2>Market Insights</h2>
      <div style={{ width: "100%", height: "100%", minHeight: "300px" }}>
        <ResponsiveContainer>
          <BarChart
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(255,255,255,0.1)"
            />
            <XAxis dataKey="name" stroke="#e0e0e0" />
            <YAxis stroke="#e0e0e0" />
            <Tooltip
              contentStyle={{
                backgroundColor: "#1e1e1e",
                borderColor: "#333",
                color: "#fff",
              }}
              itemStyle={{ color: "#fff" }}
            />
            <Legend />
            <Bar dataKey="price" name="Price ($/ton)" fill="#bb86fc" />
            <Bar dataKey="demand" name="Demand Index" fill="#03dac6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p
        style={{
          textAlign: "center",
          marginTop: "1rem",
          fontStyle: "italic",
          color: "#999",
        }}
      >
        Real-time market data visualization.
      </p>
    </div>
  );
}
