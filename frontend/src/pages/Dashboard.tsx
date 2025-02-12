import React, { useState } from "react";

interface StockData {
  stock_data: Record<string, any>;
  news: { title: string; url: string }[];
  prediction: string;
}

const Dashboard: React.FC = () => {
  const [symbol, setSymbol] = useState<string>("");
  const [data, setData] = useState<StockData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleSearch = async () => {
    if (!symbol.trim()) return;

    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await fetch(
        `http://localhost:5000/stocks/analyze?symbol=${symbol}`
      );
      const result = await response.json();

      if (response.ok) {
        setData(result);
      } else {
        setError(result.error || "Error fetching stock data.");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white shadow-md rounded-lg">
      <h1 className="text-2xl font-bold mb-4 text-center">
        Stock Analysis Dashboard
      </h1>
      <div className="flex items-center space-x-2 mb-4">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          placeholder="Enter Stock Symbol (e.g., AAPL, TSLA)"
          className="border p-2 flex-grow rounded-md"
        />
        <button
          onClick={handleSearch}
          className={`px-4 py-2 rounded-md text-white ${
            loading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"
          }`}
          disabled={loading}
        >
          {loading ? "Loading..." : "Search"}
        </button>
      </div>
      {error && <p className="text-red-500 text-center">{error}</p>}
      {data && (
        <div className="mt-4 p-4 border rounded-lg shadow-md">
          <h2 className="text-xl font-semibold">
            Stock Analysis for {symbol}
          </h2>
          <div className="mt-2">
            <h3 className="font-semibold">Stock Data:</h3>
            <pre className="bg-gray-100 p-2 rounded text-sm overflow-x-auto">
              {JSON.stringify(data.stock_data, null, 2)}
            </pre>
          </div>
          <div className="mt-2">
            <h3 className="font-semibold">Latest News:</h3>
            <ul className="list-disc pl-5 space-y-1">
              {data.news.map((article, index) => (
                <li key={index}>
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline"
                  >
                    {article.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div className="mt-2">
            <h3 className="font-semibold">Prediction:</h3>
            <p className="text-lg font-bold">{data.prediction}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;