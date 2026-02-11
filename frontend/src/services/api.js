import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const sendMessage = async (message, context = {}) => {
  try {
    const response = await apiClient.post('/chat', {
      message,
      context,
    });
    return response.data;
  } catch (error) {
    console.error('Chat error:', error);
    throw error;
  }
};

// Flight Search
export const searchFlights = async (query, context) => {
  try {
    const response = await apiClient.post('/flights/search', {
      query,
      context,
    });
    return response.data;
  } catch (error) {
    console.error('Flight search error:', error);
    throw error;
  }
};

// Visa Requirements
export const getVisaRequirements = async (query, context) => {
  try {
    const response = await apiClient.post('/visa/requirements', {
      query,
      context,
    });
    return response.data;
  } catch (error) {
    console.error('Visa requirements error:', error);
    throw error;
  }
};

// Email Draft
export const draftEmail = async (query, context) => {
  try {
    const response = await apiClient.post('/email/draft', {
      query,
      context,
    });
    return response.data;
  } catch (error) {
    console.error('Email draft error:', error);
    throw error;
  }
};

// Guide & Itinerary
export const getGuide = async (query, context) => {
  try {
    const response = await apiClient.post('/guide/itinerary', {
      query,
      context,
    });
    return response.data;
  } catch (error) {
    console.error('Guide error:', error);
    throw error;
  }
};

// Trip Management
export const createTrip = async (tripData) => {
  try {
    const response = await apiClient.post('/trip/create', tripData);
    return response.data;
  } catch (error) {
    console.error('Trip creation error:', error);
    throw error;
  }
};

export default apiClient;
