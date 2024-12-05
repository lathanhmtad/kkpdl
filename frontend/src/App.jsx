import { useState } from 'react'
import Sidebar from './components/sidebar'
import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css'

import './App.css'
import Teams from './components/teams';
import Correlation from './components/correlation';
import Spider from './components/spider';
import Predication from './components/predication';
import Rank from './components/Rank';

export default function App() {
  const [expanded, setExpanded] = useState(true)

  return (
    <BrowserRouter>
      <div>
        <Sidebar expanded={expanded} setExpanded={setExpanded} />
        <div style={{ marginLeft: `${expanded ? '240px' : '64px'}`, transition: 'linear 0.2s' }}>
          <Routes>
            <Route path='/' element={<Teams />} />
            <Route path="/correlation" element={<Correlation />} />
            <Route path="/spider-chart" element={<Spider />} />
            <Route path="/predication" element={<Predication />} />
            <Route path="/rank" element={<Rank />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}