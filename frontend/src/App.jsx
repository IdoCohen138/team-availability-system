import React, { useEffect, useState } from "react";
import Login from "./pages/Login.jsx";
import Statuses from "./pages/Statuses.jsx";
import { setAuth } from "./api";


export default function App() {
     const [token, setToken] = useState(localStorage.getItem("token"));
     const [isLoading, setIsLoading] = useState(true);


     useEffect(() => {
          const initializeAuth = async () => {
               await setAuth(token);
               setIsLoading(false);
          };
          initializeAuth();
     }, [token]);


     if (isLoading) {
          return <div>Loading...</div>;
     }

     if (!token) return <Login onLogin={(t) => { localStorage.setItem("token", t); setToken(t); }} />;
     return <Statuses onLogout={() => { localStorage.removeItem("token"); setToken(null); }} />;
}