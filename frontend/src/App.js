import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import TripPlanner from './components/TripPlanner';
import './App.css';

function App() {
  const [tripStarted, setTripStarted] = useState(false);
  const [currentTrip, setCurrentTrip] = useState(null);

  const handleTripCreate = (tripData) => {
    setCurrentTrip(tripData);
    setTripStarted(true);
  };

  return (
    <div className="app">
      {!tripStarted ? (
        <TripPlanner onTripCreate={handleTripCreate} />
      ) : (
        <ChatInterface currentTrip={currentTrip} />
      )}
    </div>
  );
}

export default App;
