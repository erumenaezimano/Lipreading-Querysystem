import React from 'react';
import styles from '../constants/styles'; // Update the path as needed

const Button = () => (
  <button
    type="button"
    className={`${styles.customButton} ${styles.popinsFont} text-lg text-white bg-gradient-to-r from-black to-black rounded-[10px] outline-none`}
    style={{
      boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
    }}
  >
    Get Started
  </button>
);

export default Button;




