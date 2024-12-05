import { useEffect } from "react";
import CorrelationChart from "./charts/correlation_chart";
import { useState } from "react";
import { environment } from "../utils/util";

export default function Correlation() {
  const [correlationData, setCorrelationData] = useState([])

  const getCorr = async () => {
    const response = await fetch(`${environment.BACKEND_URL}/api/correlation`)

    const data = await response.json()
    if (response.ok) {
      setCorrelationData(data)
    }
  }

  useEffect(() => {
    getCorr()
  }, [])

  return <div>
    <CorrelationChart correlationData={correlationData}/>
  </div>
}