import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function DynamicChart({ spots }) {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Occupied Spots',
        data: [],
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.5)',
      },
    ],
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const time = new Date().toLocaleTimeString();
      const occupiedCount = spots.filter(Boolean).length; // Count how many spots are true (occupied)
      setChartData(prevData => ({
        labels: [...prevData.labels, time].slice(-15), // Keep last 15 data points
        datasets: [{
          ...prevData.datasets[0],
          data: [...prevData.datasets[0].data, occupiedCount].slice(-15),
        }],
      }));
    }, 1000); // Update chart every 1 second

    return () => clearInterval(interval);
  }, [spots]);

  return <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />;
}

function App() {
  const [spots, setSpots] = useState([false, false]); // Initially, both spots are not occupied

  useEffect(() => {
    const interval = setInterval(() => {
      setSpots(spots => spots.map(() => Math.random() < 0.5)); // Randomly occupy spots
    }, 5000); // Change status every 5 second

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Parking Lot Status</h1>
        <div className="parking-lot">
          {spots.map((isOccupied, index) => (
            <div key={index} className={`spot ${isOccupied ? 'occupied' : 'available'}`}>
              Spot {index + 1}: {isOccupied ? 'Occupied' : 'Available'}
            </div>
          ))}
        </div>
        <h2>Live Spot Occupancy Chart</h2>
        <div style={{ width: '600px', height: '400px' }}>
          <DynamicChart spots={spots} />
        </div>
      </header>
    </div>
  );
}

export default App;
