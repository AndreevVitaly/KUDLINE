import React from 'react'
import ReactDOM from 'react-dom/client'
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import {AppErrorBoundary} from './components/common/AppErrorBoundary'
import {Layout} from './components/layout/Layout'
import {AboutPage} from './pages/AboutPage'
import {AdvantagesPage} from './pages/AdvantagesPage'
import {ContactsPage} from './pages/ContactsPage'
import {HomeOverviewPage} from './pages/HomeOverviewPage'
import {LegalContentPage} from './pages/LegalContentPage'
import {NotFoundPage} from './pages/NotFoundPage'
import {ProductionRefinedPage} from './pages/ProductionRefinedPage'
import {ProjectDetailPage} from './pages/ProjectDetailPage'
import {ProjectsRefinedPage} from './pages/ProjectsRefinedPage'
import {RequestPage} from './pages/RequestPage'
import {ServiceDetailPage} from './pages/ServiceDetailPage'
import {ServicesPage} from './pages/ServicesPage'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AppErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout/>}>
          <Route path="/" element={<HomeOverviewPage/>}/>
          <Route path="/about" element={<AboutPage/>}/>
          <Route path="/services" element={<ServicesPage/>}/>
          <Route path="/services/:slug" element={<ServiceDetailPage/>}/>
          <Route path="/production" element={<ProductionRefinedPage/>}/>
          <Route path="/projects" element={<ProjectsRefinedPage/>}/>
          <Route path="/projects/:slug" element={<ProjectDetailPage/>}/>
          <Route path="/advantages" element={<AdvantagesPage/>}/>
          <Route path="/contacts" element={<ContactsPage/>}/>
          <Route path="/request" element={<RequestPage/>}/>
          <Route path="/privacy" element={<LegalContentPage kind="privacy"/>}/>
          <Route path="/requisites" element={<LegalContentPage kind="requisites"/>}/>
          <Route path="*" element={<NotFoundPage/>}/>
          </Route>
        </Routes>
      </BrowserRouter>
    </AppErrorBoundary>
  </React.StrictMode>,
)

