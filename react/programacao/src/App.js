import logo from './logo.svg';
import './App.css';
import Header from './components/Header.js'
import Linha from './components/Linha'
import React from 'react';

function App() {
  return (
    <React.Fragment>
      <Header />
      <Linha />
    </React.Fragment>
  );
}

export default App;
