import { useEffect, useState } from "react"
import { environment } from "../utils/util"
import TrendChart from "./charts/trend"
import Seasonal from "./charts/seasonal"
import WeeklyStats from "./charts/weekly_stats"
import DaiLy from "./charts/daily"
import Monthly from "./charts/monthly"

export default function Teams() {
  const [teams, setTeams] = useState([])
  const [dataTrend, setDataTrend] = useState(null)
  const [dataSeasonal, setDataSeasonal] = useState(null)
  const [dataWeekly, setDataWeekly] = useState(null)
  const [dataDaily, setDataDaily] = useState(null)
  const [dataMonthly, setDataMonthly] = useState(null)

  const getTeams = async () => {
    const response = await fetch(`${environment.BACKEND_URL}/api/teams`)

    const data = await response.json()

    if (response.ok) {
      setTeams(data.teams)
    }
  }

  useEffect(() => {
    getTeams()
  }, [])

  const handleChange = async (event) => {
    const team_id = event.target.value

    const response1 = await fetch(`${environment.BACKEND_URL}/api/trend/${team_id}`)
    const response2 = await fetch(`${environment.BACKEND_URL}/api/seasonal/${team_id}`)
    const response3 = await fetch(`${environment.BACKEND_URL}/api/weekly/${team_id}`)
    const response4 = await fetch(`${environment.BACKEND_URL}/api/daily/${team_id}`)
    const response5 = await fetch(`${environment.BACKEND_URL}/api/monthly/${team_id}`)

    const data1 = await response1.json()
    const data2 = await response2.json()
    const data3 = await response3.json()
    const data4 = await response4.json()
    const data5 = await response5.json()
    setDataTrend(data1)
    setDataSeasonal(data2)
    setDataWeekly(data3)
    setDataDaily(data4)
    setDataMonthly(data5)
  }

  return <div>
    <select onChange={handleChange}>
      <option>Chọn một đội--</option>
      {teams.map(team => <option value={team.team_id} key={team.team_id}>{team.team_name}</option>
      )}
    </select>
    {dataWeekly && <DaiLy dailyData={dataDaily} />}
    {dataWeekly && <WeeklyStats data={dataWeekly} />}
    {dataMonthly && <Monthly monthlyData={dataMonthly} />}
    {dataTrend && <TrendChart data={dataTrend} />}
    {dataSeasonal && <Seasonal chartData={dataSeasonal} />}
  </div>
}