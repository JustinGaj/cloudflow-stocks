import React, { useEffect, useState } from "react";
import StockChart from "./components/StockChart";

export default function App() {
  const [top, setTop] = useState([]);

  useEffect(() => {
    fetch("/api/top")
      .then((res) => res.json())
      .then(data => setTop(data.top || []))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h1>CloudFlowStocks — Top Movers</h1>
      <StockChart data={top.slice(0, 10)} />
      <h2>Top List</h2>
      <table border="1" cellPadding="6">
        <thead><tr><th>Name</th><th>Close</th><th>Open</th><th>% change</th></tr></thead>
        <tbody>
        {top.map((t,i) => (
          <tr key={i}>
            <td>{t.Name}</td>
            <td>{t.Close}</td>
            <td>{t.Open}</td>
            <td>{t.change ? t.change.toFixed(2) : "0.00"}</td>
          </tr>
        ))}
        </tbody>
      </table>
    </div>
  );
}
