//import logo from './logo.svg';
import './App.css';
import Titulo from './components/Titulo.js'
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
        <Route path="programacao">
          <Route path=":igreja" element={<Programacao/>}/> 
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
