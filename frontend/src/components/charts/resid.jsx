import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

export default function Resid({ selectedFixture }) {
  const [residData, setResidData] = useState({ months: [], wins_resid: [], draws_resid: [], losses_resid: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Tạo hàm async để gọi API Resid
    const fetchResidData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5000/api/resid?team_name=${selectedFixture.team_name}&season=2023`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setResidData({
          months: data.month,
          wins_resid: data.wins_resid,
          draws_resid: data.draws_resid,
          losses_resid: data.losses_resid
        });
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchResidData(); // Gọi hàm fetchResidData
  }, [selectedFixture]);

  return (
    <div>
      <h2>Biểu đồ Resid của {selectedFixture.home_team} (Mùa 2023)</h2>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <Plot
          data={[
            {
              x: residData.months,
              y: residData.wins_resid,
              mode: 'markers',
              name: 'Wins Residuals',
              marker: { color: 'blue' }
            },
            {
              x: residData.months,
              y: residData.draws_resid,
              mode: 'markers',
              name: 'Draws Residuals',
              marker: { color: 'orange' }
            },
            {
              x: residData.months,
              y: residData.losses_resid,
              mode: 'markers',
              name: 'Losses Residuals',
              marker: { color: 'green' }
            }
          ]}
          layout={{
            title: `${selectedFixture.home_team} Residual Performance`,
            xaxis: { title: 'Month' },
            yaxis: { title: 'Residuals' },
            shapes: [
              {
                type: 'line',
                x0: residData.months[0],
                x1: residData.months[residData.months.length - 1],
                y0: 0,
                y1: 0,
                line: {
                  color: 'black',
                  width: 1,
                  dash: 'dash'
                }
              }
            ]
          }}
        />
      )}
    </div>
  );
}
