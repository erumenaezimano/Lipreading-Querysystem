import React from 'react'

import {Footer, Header, Home} from './containers';
import {Navbar, Getstarted} from './components';
import './App.css';

const App = () => (
  <div>
      <Navbar />
      <Header /> 
      <Home />
      <Getstarted />
      <Footer/>
  </div>
);

export default App;