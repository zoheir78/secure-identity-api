import React, { useState, useEffect } from "react";
import axios from "axios";

export default function AdminRules() {
  const accessToken = localStorage.getItem("access");
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");
  const [rules, setRules] = useState([]);
  const [successMessage, setSuccessMessage] = useState("");


  // Fetch user list on page load
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8081/api/admin/users/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      .then((res) => {
        setUsers(res.data);
        if (res.data.length > 0) {
          setSelectedUser(res.data[0].username);
        }
      });
  }, [accessToken]);

  // Fetch visibility rules when selectedUser changes
  useEffect(() => {
    if (!selectedUser) return;
    axios
      .get(
        `http://127.0.0.1:8081/api/admin/users/${selectedUser}/rules/`,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      )
      .then((res) => {
        setRules(res.data);
      });
  }, [selectedUser, accessToken]);

  // Handle checkbox toggle
  const handleToggle = (ruleId, field) => {
    setRules((prev) =>
      prev.map((rule) =>
        rule.id === ruleId ? { ...rule, [field]: !rule[field] } : rule
      )
    );
  };

  // Save rules (PUT)
  const handleSave = () => {
    axios
        .put(
        `http://127.0.0.1:8081/api/admin/users/${selectedUser}/rules/`,
        rules,
        { headers: { Authorization: `Bearer ${accessToken}` } }
        )
        .then(() => {
        setSuccessMessage("Changes saved successfully");

        // Clear the message after 3 seconds
        setTimeout(() => setSuccessMessage(""), 3000);
        });
    };


  return (
    <div style={{ padding: "20px" }}>
      <h2>Admin – Manage Visibility Rules</h2>

      {/* Select User */}
      <div>
        <label>Select User: </label>
        <select
          value={selectedUser}
          onChange={(e) => setSelectedUser(e.target.value)}
        >
          {users.map((u) => (
            <option key={u.username} value={u.username}>
              {u.username}
            </option>
          ))}
        </select>
      </div>

      {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}

      {/* Rules Table */}
      <table style={{ marginTop: "20px", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Context</th>
            <th>Legal</th>
            <th>Preferred</th>
            <th>Username</th>
          </tr>
        </thead>
        <tbody>
          {rules.map((rule) => (
            <tr key={rule.id}>
              <td>{rule.context}</td>
              <td>
                <input
                  type="checkbox"
                  checked={rule.show_legal_name}
                  onChange={() => handleToggle(rule.id, "show_legal_name")}
                />
              </td>
              <td>
                <input
                  type="checkbox"
                  checked={rule.show_preferred_name}
                  onChange={() => handleToggle(rule.id, "show_preferred_name")}
                />
              </td>
              <td>
                <input
                  type="checkbox"
                  checked={rule.show_username}
                  onChange={() => handleToggle(rule.id, "show_username")}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button style={{ marginTop: "15px" }} onClick={handleSave}>
        Save Changes
      </button>

      <button
        style={{ marginLeft: "10px" }}
        onClick={() => (window.location.href = "/dashboard")}>
        Back to Dashboard
      </button>




    </div>
  );
}
