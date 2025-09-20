import React from "react";


export default function StatusBadge({ status }) {
     const isVacation = status === "On Vacation";
     const styles = {
          padding: "4px 8px",
          borderRadius: 8,
          background: isVacation ? "#e5e7eb" : "#e0f2fe",
          color: isVacation ? "#4b5563" : "#0c4a6e",
          fontSize: 12,
     };
     return <span style={styles}>{status}</span>;
}