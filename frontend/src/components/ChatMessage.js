import React from 'react';
import '../styles/ChatMessage.css';

const ChatMessage = ({ message }) => {
  const { text, sender, data, isError, timestamp } = message;

  const renderData = () => {
    if (!data) return null;

    if (data.flights && Array.isArray(data.flights)) {
      return (
        <div className="data-display flights">
          <h4>Available Flights:</h4>
          {data.flights.map((flight) => (
            <div key={flight.id} className="flight-item">
              <div className="flight-header">
                <span className="airline">{flight.airline}</span>
                <span className="price">${flight.price}</span>
              </div>
              <div className="flight-details">
                <span>{flight.departure} → {flight.arrival}</span>
                <span>Duration: {flight.duration}</span>
                <span>Stops: {flight.stops}</span>
                <span>Class: {flight.seat_class}</span>
              </div>
            </div>
          ))}
        </div>
      );
    }

    if (data.requirements) {
      return (
        <div className="data-display visa">
          <h4>Visa Requirements:</h4>
          <p><strong>Processing Time:</strong> {data.requirements.processing_days} days</p>
          <p><strong>Fee:</strong> ${data.requirements.fee}</p>
          <h5>Required Documents:</h5>
          <ul>
            {data.requirements.required_docs.map((doc, idx) => (
              <li key={idx}>{doc}</li>
            ))}
          </ul>
        </div>
      );
    }

    if (data.draft_email) {
      return (
        <div className="data-display email">
          <h4>Email Draft:</h4>
          <div className="email-preview">
            <p><strong>To:</strong> {data.draft_email.to}</p>
            <p><strong>Subject:</strong> {data.draft_email.subject}</p>
            <p><strong>Body:</strong></p>
            <pre>{data.draft_email.body}</pre>
          </div>
        </div>
      );
    }

    if (data.must_see_attractions) {
      return (
        <div className="data-display guide">
          <h4>City Guide - {data.destination}</h4>
          <h5>Must-See Attractions:</h5>
          <ul>
            {data.must_see_attractions.map((attraction, idx) => (
              <li key={idx}>
                {attraction.name} - {attraction.duration} ({attraction.cost})
              </li>
            ))}
          </ul>
          {data.local_tips && (
            <>
              <h5>Local Tips:</h5>
              <ul>
                {data.local_tips.map((tip, idx) => (
                  <li key={idx}>{tip}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      );
    }

    return null;
  };

  return (
    <div className={`message message-${sender} ${isError ? 'error' : ''}`}>
      <div className="message-content">
        <p className="message-text">{text}</p>
        {renderData()}
      </div>
      <span className="message-time">
        {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </span>
    </div>
  );
};

export default ChatMessage;
