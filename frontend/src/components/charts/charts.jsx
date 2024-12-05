import { formatDate } from "../../utils/date-utils";
import Trend from "./trend";
import Seasonal from "./seasonal";
import Resid from "./resid";

export default function Charts({ selectedFixture }) {


  return <div className='m-5'>
    <h6>{formatDate(selectedFixture.match_date)}</h6>
    <h2>{selectedFixture.home_team} vs {selectedFixture.away_team}</h2>

    <div className='mt-5'>
      <div className="my-5">
        <Trend selectedFixture={selectedFixture} />
      </div>
      <div className="my-5">
        {/* <Seasonal selectedFixture={selectedFixture} /> */}
      </div>
      <div className="my-5">
        {/* <Resid selectedFixture={selectedFixture} /> */}
      </div>
    </div>
  </div>
}