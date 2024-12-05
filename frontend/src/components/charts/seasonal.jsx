import Plot from "react-plotly.js";

export default function Seasonal({ chartData }) {
  // Chuyển dữ liệu thành dạng dùng cho Plotly
  const dates = chartData.map((item) => {
    const date = new Date(item.match_date); // Chuyển đổi chuỗi thành đối tượng Date
    return date.toISOString().split("T")[0]; // Định dạng lại thành YYYY-MM-DD
  });
  const seasonalValues = chartData.map((item) => item.seasonal); // Mảng giá trị `seasonal`

  return (
    <Plot
      data={[
        {
          x: dates, // Trục X là ngày
          y: seasonalValues, // Trục Y là giá trị seasonal
          type: "scatter", // Biểu đồ dạng đường
          mode: "lines+markers", // Đường nối và marker
          marker: { size: 6 }, // Kích thước marker
        },
      ]}
      layout={{
        title: "Seasonal pattern goals", // Tiêu đề biểu đồ
        xaxis: { title: "Date" }, // Tiêu đề trục X
        yaxis: { title: "Seasonal Value" }, // Tiêu đề trục Y
      }}
      style={{ width: "100%", height: "500px" }} // Kích thước biểu đồ
    />
  );
};
