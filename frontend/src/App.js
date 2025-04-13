import React from 'react';
import ApiTest from './components/ApiTest';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Market Research Bot</h1>
        <p>A lightweight, real-time market intelligence tool for product builders</p>
      </header>
      <main>
        <ApiTest />
      </main>
      <footer>
        <p>© 2025 Project Crux - Market Research Bot</p>
      </footer>
    </div>
  );
}

export default App;
