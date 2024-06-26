// src/AppRouter.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import MainFeed from './components/mainFeed';

const AppRouter = () => (
  <Router>
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/newsfeed" element={<MainFeed />} />
      <Route path="/" element={<Login />} />
    </Routes>
  </Router>
);

export default AppRouter;
