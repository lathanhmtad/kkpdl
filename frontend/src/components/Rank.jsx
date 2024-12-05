import { useEffect, useState } from "react"
import { environment } from "../utils/util"

export default function Rank() {
  const [teams, setTeams] = useState([])

  const [pos, setPos] = useState(null)

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


  const handleChange1 = async (event) => {
    const response = await fetch(`${environment.BACKEND_URL}/api/rank/${event.target.value}`)

    const data = await response.json()
    console.log(data.team_ids)
    console.log(data.team_ids.indexOf(+event.target.value))
    setPos(data.team_ids.indexOf(+event.target.value) + 1)
  }

  return <div className="ranking-container">
    <select className="ranking-select" onChange={handleChange1}>
      <option>Chọn một đội--</option>
      {teams.map((team) => (
        <option className="ranking-option" value={team.team_id} key={team.team_id}>
          {team.team_name}
        </option>
      ))}
    </select>

    {pos && (
      <p className="ranking-result">
        Thứ hạng: <strong className="ranking-strong">{pos}</strong>
      </p>
    )}
  </div>
}