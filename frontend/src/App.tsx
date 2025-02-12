import React from "react";
import StockChart from "./components/StockChart";
import NewsFeed from "./components/NewsFeed";

const App: React.FC = () => {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold text-center">Stock Predictor LLM</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <StockChart />
                <NewsFeed />
            </div>
        </div>
    );
};

export default App;