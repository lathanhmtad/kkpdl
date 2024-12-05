import { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { environment } from '../../utils/util';

const SpiderChart = ({ home, away }) => {
  const [data, setData] = useState([]);
  const [labels, setLabels] = useState([]);

  const getSpider = () => {
    fetch(`${environment.BACKEND_URL}/api/spider/${home}/${away}`)
      .then((response) => response.json())
      .then((records) => {
        if (records.length > 0) {
          const firstRecord = records[0];
          setLabels(Object.keys(firstRecord));
          const homeValues = Object.values(firstRecord).map((val) => val[0]);
          const awayValues = Object.values(firstRecord).map((val) => val[1]);

          setData([
            {
              type: 'scatterpolar',
              r: [...homeValues, homeValues[0]],
              theta: [...Object.keys(firstRecord), Object.keys(firstRecord)[0]],
              fill: 'toself',
              name: 'Home',
              line: { color: 'red' },
            },
            {
              type: 'scatterpolar',
              r: [...awayValues, awayValues[0]],
              theta: [...Object.keys(firstRecord), Object.keys(firstRecord)[0]],
              fill: 'toself',
              name: 'Away',
              line: { color: 'blue' },
            },
          ]);
        }
      })
      .catch((error) => console.error('Error fetching spider chart data:', error));
  }

  useEffect(() => {
    if (home && away) {
      getSpider()
    }
  }, [home, away]);

  console.log(labels)

  return (
    <div>
      <h2>Spider Chart: Home vs Away</h2>
      <Plot
        data={data}
        layout={{
          polar: {
            radialaxis: { visible: true, range: [0, 10] },
          },
          title: 'Home vs Away Statistics',
        }}
      />
    </div>
  );
};

export default SpiderChart;
