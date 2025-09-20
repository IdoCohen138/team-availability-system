import React, { useState } from "react";
import { api, setAuth } from "../api";


export default function Login({ onLogin }) {
const [username, setUsername] = useState("");
const [password, setPassword] = useState("");
const [error, setError] = useState("");


const submit = async (e) => {
     e.preventDefault();
     setError("");
     try {
          const form = new URLSearchParams();
          form.append("username", username);
          form.append("password", password);
          const { data } = await api.post("/api/auth/login", form, {
               headers: { "Content-Type": "application/x-www-form-urlencoded" },
          });
          await setAuth(data.access_token);
          onLogin(data.access_token);
     } catch (err) {
          setError("Invalid credentials");
     }
};


return (
     <div style={{ maxWidth: 360, margin: "80px auto", fontFamily: "sans-serif" }}>
          <h2>Welcome to MyWorkStatus</h2>
          <form onSubmit={submit}>
          <div>
               <label>Username</label>
               <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div>
               <label>Password</label>
               <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit">Login</button>
          {error && <p style={{ color: "red" }}>{error}</p>}
          </form>
     </div>
     );
}