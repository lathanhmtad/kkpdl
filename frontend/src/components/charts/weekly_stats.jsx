import Plot from 'react-plotly.js';

const WeeklyStats = ({ data }) => {
  // Chuyển đổi dữ liệu từ API thành định dạng sử dụng trong Plot.js
  const weeks = data.map((item) => item.week);
  const goals = data.map((item) => item.goals_home);
  const corners = data.map((item) => item.corner_home);
  const cards = data.map((item) => item.yellow_cards_home + item.red_cards_home);

  return (
    <div>
      <Plot
        data={[
          {
            x: weeks,
            y: goals,
            type: 'bar',
            name: 'Goals (Home)',
          },
          {
            x: weeks,
            y: corners,
            type: 'bar',
            name: 'Corners (Home)',
          },
          {
            x: weeks,
            y: cards,
            type: 'bar',
            name: 'Cards (Yellow + Red)',
          },
        ]}
        layout={{
          title: 'Weekly Statistics (Goals, Corners, Cards)',
          barmode: 'group',
          width: '1200'
        }}
      />
    </div>
  );
};

export default WeeklyStats;
