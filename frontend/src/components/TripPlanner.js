import React from 'react';
import '../styles/TripPlanner.css';

const TripPlanner = ({ onTripCreate }) => {
  const [formData, setFormData] = React.useState({
    destination: '',
    startDate: '',
    endDate: '',
    budget: '',
    budgetTier: 'moderate',
    travelers: '1',
    interests: [],
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onTripCreate(formData);
  };

  return (
    <div className="trip-planner">
      <h2>Let's Plan Your Trip</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Destination</label>
          <input
            type="text"
            name="destination"
            value={formData.destination}
            onChange={handleChange}
            placeholder="e.g., Paris, Bangkok, Tokyo"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Start Date</label>
            <input
              type="date"
              name="startDate"
              value={formData.startDate}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>End Date</label>
            <input
              type="date"
              name="endDate"
              value={formData.endDate}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Budget (USD)</label>
            <input
              type="number"
              name="budget"
              value={formData.budget}
              onChange={handleChange}
              placeholder="e.g., 1000"
              required
            />
          </div>
          <div className="form-group">
            <label>Budget Tier</label>
            <select name="budgetTier" value={formData.budgetTier} onChange={handleChange}>
              <option value="cheap">Budget</option>
              <option value="moderate">Moderate</option>
              <option value="luxury">Luxury</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Travelers</label>
          <input
            type="number"
            name="travelers"
            value={formData.travelers}
            onChange={handleChange}
            min="1"
            max="10"
          />
        </div>

        <button type="submit" className="btn-submit">
          Start Planning
        </button>
      </form>
    </div>
  );
};

export default TripPlanner;
