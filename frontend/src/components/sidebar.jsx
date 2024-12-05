import '@trendmicro/react-sidenav/dist/react-sidenav.css'

import SideNav, { NavItem, NavIcon, NavText } from '@trendmicro/react-sidenav'
import { useLocation, useNavigate } from 'react-router-dom'

export default function Sidebar(props) {
  const { expanded, setExpanded } = props

  const navigate = useNavigate()
  const location = useLocation()

  return (
    <div className='sidebar'>
      <SideNav
        onSelect={selected => navigate(selected)}
        expanded={expanded}
        onToggle={() => setExpanded(!expanded)}
      >
        <SideNav.Toggle />
        <SideNav.Nav defaultSelected={location.pathname}>
          <NavItem eventKey="/">
            <NavIcon>
              <i className="fa fa-fw fa-home" style={{ fontSize: '1.75em' }} />
            </NavIcon>
            <NavText>
              Dashboard
            </NavText>
          </NavItem>
          <NavItem eventKey="/correlation">
            <NavIcon>
              <i className="fa fa-fw fa-home" style={{ fontSize: '1.75em' }} />
            </NavIcon>
            <NavText>
              Correlation
            </NavText>
          </NavItem>
          <NavItem eventKey="/spider-chart">
            <NavIcon>
              <i className="fa fa-fw fa-home" style={{ fontSize: '1.75em' }} />
            </NavIcon>
            <NavText>
              Spider chart
            </NavText>
          </NavItem>
          <NavItem eventKey="/predication">
            <NavIcon>
              <i className="fa fa-fw fa-home" style={{ fontSize: '1.75em' }} />
            </NavIcon>
            <NavText>
              Predication
            </NavText>
          </NavItem>
          <NavItem eventKey="/rank">
            <NavIcon>
              <i className="fa fa-fw fa-home" style={{ fontSize: '1.75em' }} />
            </NavIcon>
            <NavText>
              Rank
            </NavText>
          </NavItem>
        </SideNav.Nav>
      </SideNav>
    </div>
  )
}