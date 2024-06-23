// src/Register.js
import React, { useState } from 'react';
import axios from 'axios';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8003/users/register/', { email, password });
      if (response && response.data) {
        alert(response.data.message);
      } else {
        alert('Registration successful');
      }
    } catch (error) {
      if (error.response && error.response.data) {
        alert(error.response.data.message);
      } else {
        alert('An error occurred during registration');
      }
    }
  };

  return (
    <div className="register">
      <h1>NexPulse</h1>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input
          type="email"
          placeholder="EMAIL"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
      <p>Already have an account? <a href="/login">Log in</a></p>
    </div>
  );
}

export default Register;
