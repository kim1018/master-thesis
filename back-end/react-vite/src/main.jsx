import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import MainRoutes from './Routes'
import './includes/i18n.js'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ConfigProvider theme={{ token: { colorPrimary: '#64dd17' } }}>
        <MainRoutes />
      </ConfigProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
