// src/components/Register.js

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Register.css';
import axios from "axios";

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   // Handle registration logic here
  //   console.log('Registering with:', { username, email, password });
  // };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8002/auth/register/', { email, password });
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
      <h2>Register</h2>
      <h5>Enter your details to register in NexPulse</h5>
      <form onSubmit={handleRegister}>
        <div>
          <label>Username:</label>
          <input className="labels" type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div>
          <label>Email:</label>
          <input className="labels" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label>
          <input className="labels" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Register</button>
      </form>
      <p>
        Already have an account? <Link to="/login">Login here</Link>
      </p>
    </div>
  );
}

export default Register;
