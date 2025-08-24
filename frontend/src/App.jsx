import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import AdminRules from "./pages/AdminRules";

function PrivateRoute({ children }) {
  const token = localStorage.getItem("access");
  return token ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<Navigate to="/login" />} />

        <Route
          path="/admin-dashboard"
          element={
            <PrivateRoute>
              {localStorage.getItem("isAdmin") === "true" ? (
                <AdminRules />
              ) : (
                <Navigate to="/dashboard" />
              )}
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}
