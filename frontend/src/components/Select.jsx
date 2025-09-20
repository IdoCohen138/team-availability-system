import React from "react";


export default function Select({ value, onChange, options }) {
     return (
          <select value={value} onChange={(e) => onChange(e.target.value)}>
          {options.map((o) => (
          <option key={o} value={o}>{o}</option>
          ))}
          </select>
     );
}