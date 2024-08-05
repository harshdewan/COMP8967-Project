// src/Sidebar.js
import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

const SidebarContainer = styled.div`
  width: 250px;
  height: 100vh;
  background-color: #FFEFEF;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  padding: 20px;
`;

const SidebarLink = styled(Link)`
  color: black;
  text-decoration: none;
  margin: 10px 0;
  background: white;
  border-radius: 8%;
  &:hover {
    text-decoration: underline;
  }
`;

const Sidebar = () => {
  return (
    <SidebarContainer>
      <h2>NexPulse</h2>
      <SidebarLink to="/">Home</SidebarLink>
      <SidebarLink to="/about">About</SidebarLink>
      <SidebarLink to="/services">Services</SidebarLink>
      <SidebarLink to="/contact">Contact</SidebarLink>
    </SidebarContainer>
  );
};

export default Sidebar;
