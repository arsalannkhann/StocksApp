import React, { useEffect, useState } from "react";
import StockChart from "./StockChart";
import NewsFeed from "./NewsFeed";
import { fetchData } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

interface StockData {
  stock_data: any;
  news: Array<{ title: string; description: string }>;
  prediction: string;
}

const Dashboard: React.FC = () => {
  const { token, user } = useAuth();
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [symbol, setSymbol] = useState("AAPL");

  useEffect(() => {
    const fetchStockAnalysis = async () => {
      if (!token || !user) return;
      try {
        const data = await fetchData(token, symbol);
        setStockData(data);
      } catch (error) {
        console.error("Fetch error:", error);
      }
    };
    fetchStockAnalysis();
  }, [symbol, token, user]);

  return (
    <div className="max-w-7xl mx-auto p-4">
      <h1 className="text-2xl font-bold">Stock Dashboard</h1>
      <div className="flex flex-col md:flex-row gap-4 mt-4">
        <div className="flex-1">
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            className="border p-2 rounded w-full mb-2"
            placeholder="Enter stock symbol"
          />
          {stockData && (
            <StockChart
              title={`Historical Data for ${symbol}`}
              data={stockData.stock_data}
            />
          )}
        </div>
        <div className="flex-1">
          <NewsFeed news={stockData?.news || []} />
        </div>
      </div>
      {stockData && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h2 className="text-lg font-bold">Llama2 Prediction:</h2>
          <p>{stockData.prediction}</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;