import { useEffect, useState } from "react"
import { environment } from "../utils/util"
import SpiderChart from "./charts/spider_chart"

export default function Spider() {
  const [teams, setTeams] = useState([])

  const [selectedHome, setSelectedHome] = useState(null)
  const [selectedAway, setSelectedAway] = useState(null)

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

  const handleChange1 = (event) => {
    setSelectedHome(event.target.value)
  }

  const handleChange2 = (event) => {
    setSelectedAway(event.target.value)
  }

  const handleClick = async () => {

  }

  return <div>
    <select onChange={handleChange1}>
      <option>Chọn một đội--</option>
      {teams.map(team => <option value={team.team_id} key={team.team_id}>{team.team_name}</option>
      )}
    </select>

    <select onChange={handleChange2}>
      <option>Chọn một đội--</option>
      {teams.map(team => <option value={team.team_id} key={team.team_id}>{team.team_name}</option>
      )}
    </select>

    <button onClick={handleClick}>Get</button>

    {selectedHome && selectedAway && <SpiderChart home={selectedHome} away={selectedAway}/>}
  </div>
}