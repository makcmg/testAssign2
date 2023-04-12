// components/LineChart.js
import React from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { useState } from "react";

Chart.register(CategoryScale);

function LineChart({chartData}) {
  console.log('chartData', chartData)
  const [chData, setChData] = useState({
    labels: chartData.map((data) => data.year),
    datasets: [
      {
        label: "Общая сумма заказов в этот день в $",
        data: chartData.map((data) => data.sum_order),
        backgroundColor: [
          "rgba(75,192,192,1)",
          "#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0"
        ],
        borderColor: "black",
        borderWidth: 1
      }
    ]
  });
  return (
    <div className="chart-container">
      <Line
        data={chData}
        options={{
          plugins: {
            title: {
              display: true,
              text: ""
            },
            legend: {
              display: false
            }
          }
        }}
      />
    </div>
  );
}
export default LineChart;