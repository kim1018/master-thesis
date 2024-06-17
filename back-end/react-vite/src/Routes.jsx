import React from 'react'
import { Routes, Route } from 'react-router-dom'
import App from './App'
import Detail from './detail'

const MainRoutes = () => {
  return (
    <div>
      <Routes>
        <Route exact path="/" element={<App />} />
        <Route path="/detail" element={<Detail />} />
      </Routes>
    </div>
  )
}

export default MainRoutes
