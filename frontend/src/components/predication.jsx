import { useEffect, useState } from "react"
import { environment } from "../utils/util"

export default function Prediction() {
  const [teams, setTeams] = useState([])

  const [selectedHome, setSelectedHome] = useState(null)
  const [selectedAway, setSelectedAway] = useState(null)
  const [predictions, setPredictions] = useState(null);

  const getTeams = async () => {
    const response = await fetch(`${environment.BACKEND_URL}/api/teams`)

    const data = await response.json()

    if (response.ok) {
      setTeams(data.teams)
    }
  }


  const handlePredict = () => {
    fetch(`${environment.BACKEND_URL}/api/predict/${selectedHome}/${selectedAway}`)
      .then((response) => response.json())
      .then((data) => setPredictions(data))
      .catch((error) => console.error('Error:', error));
  };

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
    handlePredict()
  }

  return (
    <div className="prediction-container">
      <div className="team-selection">
        <select onChange={handleChange1} className="team-select">
          <option>Chọn một đội--</option>
          {teams.map(team => (
            <option value={team.team_id} key={team.team_id}>{team.team_name}</option>
          ))}
        </select>

        <select onChange={handleChange2} className="team-select">
          <option>Chọn một đội--</option>
          {teams.map(team => (
            <option value={team.team_id} key={team.team_id}>{team.team_name}</option>
          ))}
        </select>
      </div>

      <button onClick={handleClick} className="predict-button">Nhận lời khuyên</button>

      {predictions && (
        <div className="predictions">
          <h3>Prediction Results</h3>
          <p>Goals (Home): {predictions.predicted_goals_home}</p>
          <p>Goals (Away): {predictions.predicted_goals_away}</p>
          <p>Corners (Home): {predictions.predicted_corners_home}</p>
          <p>Corners (Away): {predictions.predicted_corners_away}</p>
          <p>Cards (Home): {predictions.predicted_cards_home}</p>
          <p>Cards (Away): {predictions.predicted_cards_away}</p>
        </div>
      )}
    </div>
  );
}
