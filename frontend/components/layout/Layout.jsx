import React from 'react';
import Navbar from '../navbar/Navbar';
import Footer from '../../containers/footer/Footer';
//import image from '../../constants/image';
import './layout.css'; 
import { ToastContainer } from "react-toastify";

const Layout = ({ children }) => {
  return (
    <div className="layout__container">
      	<ToastContainer />
      <Navbar />
      <div className="layout__content">
  
        <div className="content">{children}</div>
      </div>
      <Footer className="footer" />
    </div>
  );
};

export default Layout;
  
