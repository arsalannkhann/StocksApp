import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

const Dashboard = () => {
  const [stockData, setStockData] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5000/prices`)
      .then((res) => res.json())
      .then((data) => setStockData(data))
      .catch(console.error);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Stock Prices</h1>
      <LineChart width={600} height={300} data={stockData}>
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="price" stroke="#8884d8" />
      </LineChart>
    </div>
  );
};

export default Dashboard;