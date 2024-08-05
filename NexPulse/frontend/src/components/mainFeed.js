// src/components/Login.js

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Login.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './Sidebar';
import Feed from './Feed';
import tulip from "./tulip.jpeg"

const MainFeed = () => {

const Home = () => <div><h1>Home</h1></div>;
const About = () => <div><h1>About</h1></div>;
const Services = () => <div><h1>Services</h1></div>;
const Contact = () => <div><h1>Contact</h1></div>;

const AppContainer = {
  display: 'flex',
};

const ContentContainer = {
  marginLeft: '250px',
  padding: '20px',
};

  return (
 <body>
    <div className="sidebar">
        <h1>NexPulse</h1>
        
      <div style={AppContainer}>
        <Sidebar />
        <div style={ContentContainer}>
          {/* <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/services" element={<Services />} />
            <Route path="/contact" element={<Contact />} />
          </Routes> */}
        </div>
      </div>
    
    </div>
    <div className="main-content">
            <Feed />

    </div>
    <div className="sidebar-right">
        <section className="suggested-people">
            <h2>Suggested people</h2>
            <ul>
                <li>
                    <img src={tulip} alt="Profile Picture" />
                    <div>
                        <h3>Helena Hills</h3>
                        <p>@helenahills</p>
                    </div>
                </li>
                <li>
                    <img src={tulip} alt="Profile Picture" />
                    <div>
                        <h3>Charles Tran</h3>
                        <p>@charlestran</p>
                    </div>
                </li>
                <li>
                    <img src={tulip} alt="Profile Picture" />
                    <div>
                        <h3>Oscar Davis</h3>
                        <p>@oscardavis</p>
                    </div>
                </li>
                <li>
                    <img src={tulip} alt="Profile Picture" />
                    <div>
                        <h3>Daniel Jay Park</h3>
                        <p>@danielj</p>
                    </div>
                </li>
                <li>
                    <img src={tulip} alt="Profile Picture" />
                    <div>
                        <h3>Carlo Rojas</h3>
                        <p>@carloorojas</p>
                    </div>
                </li>
            </ul>
        </section>
        {/* <section className="communities">
            <h2>Communities you might like</h2>
            <ul>
                <li>
                    <h3>Design Enthusiasts</h3>
                    <p>13.2k members</p>
                </li>
                <li>
                    <h3>Photographers of SF</h3>
                    <p>2k members</p>
                </li>
                <li>
                    <h3>Marina crew</h3>
                    <p>125 members</p>
                </li>
            </ul>
        </section> */}
    </div>
</body>
  );
}

export default MainFeed;