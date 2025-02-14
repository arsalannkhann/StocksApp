import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthProvider from "./contexts/AuthContext";
import Dashboard from "./pages/Dashboard";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "/Users/arsalankhan/Desktop/StocksApp/frontend/src/utils/ProtectedRoute";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;