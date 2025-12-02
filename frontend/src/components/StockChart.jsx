import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function StockChart({ data }) {
  const labels = data.map(d => d.Name);
  const values = data.map(d => d.change ? Number(d.change.toFixed(2)) : 0);
  const chartData = {
    labels,
    datasets: [{ label: '% change', data: values }]
  };
  const options = { responsive: true, plugins: { legend: { position: 'top' } } };
  return <div style={{ width: '800px', maxWidth: '95%' }}><Bar data={chartData} options={options} /></div>;
}
