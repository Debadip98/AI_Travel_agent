import React, { useState } from 'react';
import '../styles/InputBox.css';

const InputBox = ({ onSend, disabled, context }) => {
  const [input, setInput] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);

  const suggestions = [
    "Find me a flight to Paris",
    "What are visa requirements for India?",
    "Help me draft an email to the hotel",
    "Show me a tour guide for Tokyo",
    "I'm a budget traveler",
    "Book train tickets for my trip",
  ];

  const handleSend = () => {
    if (input.trim()) {
      onSend(input);
      setInput('');
      setShowSuggestions(false);
    }
  };

  const handleSuggestion = (suggestion) => {
    setInput(suggestion);
    onSend(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="input-box">
      {showSuggestions && (
        <div className="suggestions-panel">
          <p className="suggestions-title">Quick suggestions:</p>
          <div className="suggestions-grid">
            {suggestions.map((suggestion, idx) => (
              <button
                key={idx}
                className="suggestion-btn"
                onClick={() => handleSuggestion(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          onKeyPress={handleKeyPress}
          placeholder="Tell me about your travel plans..."
          disabled={disabled}
          rows="2"
        />
        <button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          className="send-btn"
        >
          {disabled ? '...' : '→'}
        </button>
      </div>

      <div className="input-hints">
        <p>💡 Try: "I'm a budget traveler to Paris for 5 days" or ask about flights, visa, or local guides</p>
      </div>
    </div>
  );
};

export default InputBox;
