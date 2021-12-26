//import logo from './logo.svg';
import './App.css';
import Titulo from './components/Titulo.js'
import Eventos from './components/Eventos'
import React from 'react';

function App() {
  return (
    <React.Fragment>
      <Titulo />
      <Eventos />
    </React.Fragment>
  );
}

export default App;
