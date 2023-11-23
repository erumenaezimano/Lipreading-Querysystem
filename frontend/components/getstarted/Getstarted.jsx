import React from "react";
import { Link } from "react-router-dom";
import './getstarted.css';

const Getstarted = () => {
  return (
    <nav className="app__getstarted">
      <div className="app__getstarted-links">
        <ul>
          <li className="p__opensans">
          <Link to="/search/" className="button-link">Get Started</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Getstarted;
