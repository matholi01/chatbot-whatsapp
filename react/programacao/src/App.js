//import logo from './logo.svg';
import './App.css';
import Eventos from './components/Eventos'
import React from 'react';
import Programacao from './routes/programacao';

import {
  BrowserRouter as Router,
  Route,
  Routes,
  BrowserRouter
} from "react-router-dom";

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
