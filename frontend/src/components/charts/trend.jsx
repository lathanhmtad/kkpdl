import Plot from 'react-plotly.js';

const TrendChart = ({ data }) => {
  const matchDates = data.map(item => new Date(item.match_date)); 
  const goalsHome = data.map(item => item.goals_home);
  const yellowCardsHome = data.map(item => item.yellow_cards_home);
  const redCardsHome = data.map(item => item.red_cards_home);
  const cornersHome = data.map(item => item.corner_home);

  const plotData = [
    {
      x: matchDates,
      y: goalsHome,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Goals (Home)',
      marker: { symbol: 'circle' },
      line: { dash: 'solid' },
    },
    {
      x: matchDates,
      y: yellowCardsHome,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Yellow Cards (Home)',
      marker: { symbol: 'square' },
      line: { dash: 'dash' },
    },
    {
      x: matchDates,
      y: redCardsHome,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Red Cards (Home)',
      marker: { symbol: 'triangle-up', color: 'red' },
      line: { dash: 'dot' },
    },
    {
      x: matchDates,
      y: cornersHome,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Corners (Home)',
      marker: { symbol: 'diamond', color: 'green' },
      line: { dash: 'dashdot' },
    },
  ];

  return (
    <Plot
      data={plotData}
      layout={{
        title: 'Home Team Trends Over Time',
        showlegend: true,
        width: 1200,
        height: 450,
      }}
    />
  );
};

export default TrendChart;
