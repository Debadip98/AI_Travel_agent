import React, { useState, useEffect, useRef } from 'react';
import { sendMessage } from '../services/api';
import ChatMessage from './ChatMessage';
import InputBox from './InputBox';
import '../styles/ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your AI Travel Agent. I can help you plan your trip, book flights, arrange visa, and more. Where would you like to go?",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);

  const [loading, setLoading] = useState(false);
  const [tripContext, setTripContext] = useState({
    destination: null,
    start_date: null,
    end_date: null,
    budget: null,
    budget_tier: 'moderate', // cheap, moderate, luxury
  });

  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (message) => {
    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: message,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      // Send to backend
      const response = await sendMessage(message, tripContext);

      // Extract data
      let botReplyText = '';
      if (response.data && response.data.message) {
        botReplyText = response.data.message;
      } else if (response.data) {
        botReplyText = JSON.stringify(response.data, null, 2);
      } else {
        botReplyText = response.message || 'I understood your request.';
      }

      const botMessage = {
        id: messages.length + 2,
        text: botReplyText,
        sender: 'bot',
        data: response.data,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);

      // Update context if destination mentioned
      if (response.data && response.data.destination) {
        setTripContext((prev) => ({
          ...prev,
          destination: response.data.destination,
        }));
      }
    } catch (error) {
      const errorMessage = {
        id: messages.length + 2,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        isError: true,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1>🌍 AI Travel Agent</h1>
        <p>Your personal travel planning assistant</p>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {loading && (
          <div className="loading-indicator">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <InputBox
        onSend={handleSendMessage}
        disabled={loading}
        context={tripContext}
      />
    </div>
  );
};

export default ChatInterface;
