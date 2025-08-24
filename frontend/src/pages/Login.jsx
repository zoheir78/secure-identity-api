import { useState } from "react";
import axios from "axios";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // 1) Get access & refresh tokens
      const tokenRes = await axios.post("http://127.0.0.1:8081/api/token/", {
        username,
        password,
      });

      const accessToken = tokenRes.data.access;
      const refreshToken = tokenRes.data.refresh;

      // Save tokens
      localStorage.setItem("access", accessToken);
      localStorage.setItem("refresh", refreshToken);

      // 2) Get current user info via /api/me/
      const meRes = await axios.get("http://127.0.0.1:8081/api/me/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      localStorage.setItem("username", meRes.data.username);
      localStorage.setItem("isAdmin", meRes.data.is_staff ? "true" : "false");
      localStorage.setItem("profileId", meRes.data.profileId);

      // 3) Redirect to dashboard
      window.location.href = "/dashboard";
    } catch (err) {
      console.error(err);
      setError("Invalid username or password");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto" }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
