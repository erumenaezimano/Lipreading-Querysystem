import React from 'react';
import { FiFacebook, FiTwitter, FiInstagram } from 'react-icons/fi';
import './footer.css';

const Footer = () => (
  <div className="app__footer section__padding" id="login">
     <div className="app__footer-links">
      <div className="app__footer-links_contact">
        <h1 className="app__footer-headtext">Contact Us</h1>
        <p className="p__opensans white-text">Faraday Wing, LSBU, Elephant & Castle, LN5 9QA</p>
        <p className="p__opensans white-text">+44-01522-513-718</p>
        <p className="p__opensans white-text">+44 01522-203-673</p>
        <div className="app__footer-links_icons">
          <FiFacebook />
          <FiTwitter />
          <FiInstagram />
          </div>
</div>
<div className="footer__copyright">
  <p className="p__opensans white-text">2023 querysystem. All Rights reserved.</p>
</div>
</div>
</div>
);


export default Footer
