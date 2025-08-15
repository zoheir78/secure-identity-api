import React, { useState, useEffect } from "react";
import axios from "axios";

const isAdmin = localStorage.getItem("isAdmin") === "true";

export default function Dashboard() {
  const [contexts, setContexts] = useState([]);
  const [selectedContext, setSelectedContext] = useState("");
  const [identityData, setIdentityData] = useState({});
  const [loading, setLoading] = useState(false);

  const username = localStorage.getItem("username");
  const token = localStorage.getItem("access");

  // Fetch contexts when component mounts
  useEffect(() => {
    if (!username || !token) return;

    axios
      .get(`http://127.0.0.1:8081/api/identity/${username}/contexts/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setContexts(res.data.contexts);
        if (res.data.contexts.length > 0) {
          setSelectedContext(res.data.contexts[0]);
        }
      })
      .catch((err) => {
        console.error("Error fetching contexts:", err);
      });
  }, [username, token]);

  // Fetch identity info whenever selectedContext changes
  useEffect(() => {
    if (!selectedContext || !username || !token) return;

    setLoading(true);
    axios
      .get(
        `http://127.0.0.1:8081/api/identity/${username}/${encodeURIComponent(
          selectedContext
        )}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((res) => {
        setIdentityData(res.data);
      })
      .catch((err) => {
        console.error("Error fetching identity data:", err);
      })
      .finally(() => setLoading(false));
  }, [selectedContext, username, token]);

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("username");
    window.location.href = "/login";
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Welcome, {username}</h2>

      {/* Context Selector */}
      <div>
        <label>Select Context: </label>
        <select
          value={selectedContext}
          onChange={(e) => setSelectedContext(e.target.value)}
        >
          {contexts.map((context) => (
            <option key={context} value={context}>
              {context}
            </option>
          ))}
        </select>
      </div>

      {/* Identity Display */}
      <div style={{ marginTop: "20px" }}>
        {loading ? (
          <p>Loading identity info...</p>
        ) : (
          <div>
            {Object.entries(identityData).length > 0 ? (
              <ul>
                {Object.entries(identityData).map(([key, value]) => (
                  <li key={key}>
                    <strong>{key}:</strong> {value}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No data available for this context.</p>
            )}
          </div>
        )}
      </div>

      {/* Logout Button */}
      <button
        onClick={handleLogout}
        style={{
          marginTop: "20px",
          padding: "8px 12px",
          backgroundColor: "#d9534f",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Logout
      </button>

      {/* {isAdmin && (
        <button
          onClick={() => (window.location.href = "/admin-dashboard")}
          style={{ marginLeft: "10px" }}
  >
          Admin Rules
        </button>
      )} */}

      {isAdmin && (
        <button onClick={() => (window.location.href = "/admin-dashboard")}>
          Admin Rules
        </button>
      )}


    </div>
  );
}
