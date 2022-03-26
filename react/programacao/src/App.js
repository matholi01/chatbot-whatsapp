//import logo from './logo.svg';
import './App.css';
import Eventos from './components/Eventos'
import React from 'react';
import Programacao from './routes/programacao';


import axios from 'axios';

import {
  BrowserRouter as Router,
  Route,
  Routes,
  BrowserRouter
} from "react-router-dom";

// Para o deploy
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="programacao/:igreja" element={<Programacao/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
