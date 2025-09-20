import React, { useEffect, useMemo, useState } from "react";
import { api } from "../api";
import StatusBadge from "../components/StatusBadge.jsx";
import Select from "../components/Select.jsx";

export default function Statuses({ onLogout }) {
     const [me, setMe] = useState(null);
     const [statuses, setStatuses] = useState([]);
     const [myStatus, setMyStatus] = useState("Working");
     const [q, setQ] = useState("");
     const [filter, setFilter] = useState("");
     const [users, setUsers] = useState([]);
     
     const fetchAll = async () => {
          try {
               const [meRes, stRes] = await Promise.all([
                    api.get("/api/me"),
                    api.get("/api/statuses"),
               ]);
               setMe(meRes.data);
               setMyStatus(meRes.data.status);
               setStatuses(stRes.data);
          } catch (error) {
               if (error.response?.status === 401) {
                    // Token is invalid, logout
                    onLogout();
               } else {
                    console.error("Failed to fetch data:", error);
               }
          }
     };
     const fetchUsers = async () => {
          const params = {};
          if (q) params.q = q;
          if (filter) params.status = filter;
          const { data } = await api.get("/api/users", { params });
          setUsers(data.items.filter((u) => u.id !== me?.id));
          };
     const updateStatus = async (val) => {
          await api.patch("/api/me/status", { status: val });
          setMyStatus(val);
          };
     useEffect(() => { fetchAll(); }, []);
     useEffect(() => { if (me) fetchUsers(); }, [me, q, filter]);

     useEffect(() => {
          if (!me) return;
          
          // Get token from localStorage for WebSocket authentication
          const token = localStorage.getItem("token");
          if (!token) {
               console.error("No token found for WebSocket connection");
               return;
          }
          
          const wsUrl = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.hostname + ':8000/ws?token=' + encodeURIComponent(token);
          const ws = new WebSocket(wsUrl);
          
          ws.onopen = () => {
               console.log("WebSocket connected");
          };
          
          ws.onmessage = (evt) => {
               try {
                    const msg = JSON.parse(evt.data);
                    if (msg.type === "status_changed") {
                         // Update the local users list instead of refetching
                         setUsers(prevUsers => {
                              // Check if the updated user matches current filters
                              const matchesName = !q || msg.user.full_name.toLowerCase().includes(q.toLowerCase());
                              const matchesStatus = !filter || msg.user.status === filter;
                              
                              // If user exists in current list, update or remove based on filters
                              const userExists = prevUsers.some(u => u.id === msg.user.id);
                              if (userExists) {
                                   if (matchesName && matchesStatus) {
                                        // Update the user's status
                                        return prevUsers.map(user => 
                                             user.id === msg.user.id ? { ...user, status: msg.user.status } : user
                                        );
                                   } else {
                                        // Remove user from list if they no longer match filters
                                        return prevUsers.filter(user => user.id !== msg.user.id);
                                   }
                              } else {
                                   // User not in current list, add them if they match filters
                                   if (matchesName && matchesStatus) {
                                        return [...prevUsers, { id: msg.user.id, full_name: msg.user.full_name, status: msg.user.status }];
                                   }
                              }
                              return prevUsers;
                         });
                    }
               } catch (error) {
                    console.error("Failed to parse WebSocket message:", error);
               }
          };
          
          ws.onerror = (error) => {
               console.error("WebSocket error:", error);
          };
          
          ws.onclose = () => {
               console.log("WebSocket disconnected");
          };
          
          return () => ws.close();
     }, [me, q, filter]);

     return (
          <div style={{ maxWidth: 720, margin: "40px auto", fontFamily: "sans-serif" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
               <h3>Hello {me?.full_name}, you are <StatusBadge status={myStatus} />.</h3>
               <button onClick={onLogout}>Logout</button>
          </div>
          <div style={{ marginTop: 8 }}>
               <span>Update My Current Status: </span>
               <Select value={myStatus} onChange={updateStatus} options={statuses} />
          </div>
          <hr style={{ margin: "24px 0" }} />
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
               <input placeholder="search by name..." value={q} onChange={(e) => setQ(e.target.value)} />
               <select value={filter} onChange={(e) => setFilter(e.target.value)}>
                    <option value="">Filter By Status</option>
                    {statuses.map((s) => (
                         <option key={s} value={s}>{s}</option>
                    ))}
               </select>
               {/* Bonus: multi-select filter could be implemented here */}
          </div>
          
          <ul style={{ marginTop: 16, listStyle: "none", padding: 0 }}>
               {users.map((u) => (
                    <li key={u.id} style={{ padding: 8, borderBottom: "1px solid #eee", display: "flex", justifyContent: "space-between" }}>
                         <span>{u.full_name}</span>
                         <StatusBadge status={u.status} />
                    </li>
               ))}
          </ul>
          </div>
          );
     }