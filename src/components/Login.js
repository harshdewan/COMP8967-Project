// src/components/Login.js

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Login.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Logging in with:', { email, password });
  };

  return (
    <div className="login">
      <h2>Login</h2>
      <h5>Enter your email to Log-in to NexPulse</h5>
      <form onSubmit={handleSubmit}>
        <div className="labels">
          <label>Email:</label>
          <input className="labels" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="labels">
          <label>Password:</label>
          <input className="labels" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
};

export default Login;
