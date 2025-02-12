import React from "react";
import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Home from "/Users/arsalankhan/Desktop/StocksApp/frontend/src/pages/Home";
import NotFound from "/Users/arsalankhan/Desktop/StocksApp/frontend/src/pages/NotFound";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default App;