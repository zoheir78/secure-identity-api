import React, { useState, useEffect } from "react";
import axios from "axios";

export default function AdminRules() {
  const accessToken = localStorage.getItem("access");
  const [profiles, setProfiles] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState("");
  const [rules, setRules] = useState([]);
  const [successMessage, setSuccessMessage] = useState("");

  // Fetch all profiles on page load
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8081/api/profiles/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      .then((res) => {
        setProfiles(res.data);
        if (res.data.length > 0) {
          setSelectedProfile(res.data[0].id); // use profile.id 
        }
      });
  }, [accessToken]);

  // Fetch visibility rules when selectedProfile changes
  useEffect(() => {
    if (!selectedProfile) return;
    axios
      .get(
        `http://127.0.0.1:8081/api/rules/?profile=${selectedProfile}`,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      )
      .then((res) => {
        setRules(res.data);
      });
  }, [selectedProfile, accessToken]);

  // Handle checkbox toggle
  const handleToggle = (ruleId, field) => {
    setRules((prev) =>
      prev.map((rule) =>
        rule.id === ruleId ? { ...rule, [field]: !rule[field] } : rule
      )
    );
  };

  // Save rules (PUT each rule)
  const handleSave = () => {
    const updates = rules.map((rule) =>
      axios.put(
        `http://127.0.0.1:8081/api/rules/${rule.id}/`,
        rule,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      )
    );

    Promise.all(updates).then(() => {
      setSuccessMessage("Changes saved successfully");
      setTimeout(() => setSuccessMessage(""), 3000);
    });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Admin – Manage Visibility Rules</h2>

      {/* Select Profile */}
      <div>
        <label>Select Profile: </label>
        <select
          value={selectedProfile}
          onChange={(e) => setSelectedProfile(e.target.value)}
        >
          {profiles.map((p) => (
            <option key={p.id} value={p.id}>
              {p.user.username} (Profile ID: {p.id})
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
        onClick={() => (window.location.href = "/dashboard")}
      >
        Back to Dashboard
      </button>
    </div>
  );
}
