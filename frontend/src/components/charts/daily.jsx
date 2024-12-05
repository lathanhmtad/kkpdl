import Plot from 'react-plotly.js';

export default function DaiLy({ dailyData }) {

  const dailyDates = dailyData.map((item) => item.match_date);
  const dailyGoals = dailyData.map((item) => item.goals_home);
  const dailyCorners = dailyData.map((item) => item.corner_home);
  const dailyCards = dailyData.map((item) => item.yellow_cards_home + item.red_cards_home);

  return (
    <div>
      <h2>Daily Statistics</h2>
      <Plot
        data={[
          {
            x: dailyDates,
            y: dailyGoals,
            type: 'bar',
            name: 'Goals (Home)',
          },
          {
            x: dailyDates,
            y: dailyCorners,
            type: 'bar',
            name: 'Corners (Home)',
          },
          {
            x: dailyDates,
            y: dailyCards,
            type: 'bar',
            name: 'Cards (Yellow + Red)',
          },
        ]}
        layout={{
          title: 'Daily Statistics (Goals, Corners, Cards)',
          xaxis: { title: 'Date' },
          yaxis: { title: 'Count' },
          barmode: 'group',
          width: 1200
        }}
      />
    </div>
  );
};
