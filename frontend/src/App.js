import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './components/NavBar';
import Home from './containers/Home';
import Wines from './containers/Wines';
import Vineyards from './containers/Vineyards';
import Regions from './containers/Regions';
import About from './containers/About';


const App = () => {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="Content">
          <Routes>
            <Route exact path="/" element={<Home/>}></Route>
            <Route exact path="/Wines" element={<Wines/>}></Route>
            <Route exact path="/Vineyards" element={<Vineyards/>}></Route>
            <Route exact path="/Regions" element={<Regions/>}></Route>
            <Route exact path="/About" element={<About/>}></Route>
          </Routes>
        </div>

      </div>
    </Router>
  );
}

export default App;
