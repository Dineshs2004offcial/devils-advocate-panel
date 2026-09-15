import React, { useState } from "react";

function PitchForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    startup_name: "",
    problem: "",
    solution: "",
    target_market: "",
    business_model: "",
    funding_amount: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(formData);
  };

  return (
    <form className="pitch-form glass-panel" onSubmit={handleSubmit}>
      <h2>Submit Startup Pitch</h2>

      <div className="form-group">
        <label htmlFor="startup_name">Startup Name</label>
        <input
          type="text"
          id="startup_name"
          name="startup_name"
          value={formData.startup_name}
          onChange={handleChange}
          placeholder="e.g., MediVision AI"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="problem">Problem</label>
        <textarea
          id="problem"
          name="problem"
          value={formData.problem}
          onChange={handleChange}
          placeholder="Describe the problem your startup solves..."
          rows="3"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="solution">Solution</label>
        <textarea
          id="solution"
          name="solution"
          value={formData.solution}
          onChange={handleChange}
          placeholder="Describe your product or solution..."
          rows="3"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="target_market">Target Market</label>
        <input
          type="text"
          id="target_market"
          name="target_market"
          value={formData.target_market}
          onChange={handleChange}
          placeholder="e.g., Tier 1 and Tier 2 hospital networks"
        />
      </div>

      <div className="form-group">
        <label htmlFor="business_model">Business Model</label>
        <input
          type="text"
          id="business_model"
          name="business_model"
          value={formData.business_model}
          onChange={handleChange}
          placeholder="e.g., B2B SaaS annual subscription"
        />
      </div>

      <div className="form-group">
        <label htmlFor="funding_amount">Funding Amount ($)</label>
        <input
          type="number"
          id="funding_amount"
          name="funding_amount"
          value={formData.funding_amount}
          onChange={handleChange}
          placeholder="e.g., 500000"
          min="0"
          step="1000"
        />
      </div>

      <button type="submit" className="evaluate-button" disabled={loading}>
        {loading ? "Evaluating Pitch..." : "Evaluate Pitch"}
      </button>
    </form>
  );
}

export default PitchForm;
