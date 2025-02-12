import React, { useEffect, useState } from "react";
import { fetchData } from "/Users/arsalankhan/Desktop/StocksApp/frontend/src/services/api";

const Dashboard: React.FC = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const getData = async () => {
      const result = await fetchData();
      setData(result);
    };
    getData();
  }, []);

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold">Dashboard</h2>
      <pre className="mt-4 p-4 bg-gray-200 rounded">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default Dashboard;