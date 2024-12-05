import Plot from 'react-plotly.js';

const CorrelationChart = ({ correlationData }) => {
  const features = Object.keys(correlationData);
  const values = Object.values(correlationData);

  return (
    <div>
      <h2>Correlation with Match Result</h2>
      <Plot
        data={[
          {
            x: features,
            y: values,
            type: 'bar',
            marker: { color: 'skyblue' },
          },
        ]}
        layout={{
          title: 'Correlation with Match Result',
          xaxis: { title: 'Features', tickangle: 45 },
          yaxis: { title: 'Correlation' },
          margin: { t: 40, l: 60, r: 20, b: 100 },
        }}
      />
    </div>
  );
};

export default CorrelationChart;