import Plot from 'react-plotly.js';

export default function Monthly({ monthlyData }) {
  const monthlyDates = monthlyData.map((item) => item.month);
  const monthlyGoals = monthlyData.map((item) => item.goals_home);
  const monthlyCorners = monthlyData.map((item) => item.corner_home);
  const monthlyCards = monthlyData.map((item) => item.yellow_cards_home + item.red_cards_home);

  return (
    <div>
      <Plot
        data={[
          {
            x: monthlyDates,
            y: monthlyGoals,
            type: 'bar',
            name: 'Goals (Home)',
          },
          {
            x: monthlyDates,
            y: monthlyCorners,
            type: 'bar',
            name: 'Corners (Home)',
          },
          {
            x: monthlyDates,
            y: monthlyCards,
            type: 'bar',
            name: 'Cards (Yellow + Red)',
          },
        ]}
        layout={{
          title: 'Monthly Statistics (Goals, Corners, Cards)',
          xaxis: { title: 'Month' },
          yaxis: { title: 'Count' },
          barmode: 'group',
          width: 1200
        }}
      />
    </div>
  );
};
