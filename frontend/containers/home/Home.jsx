import React from 'react';
import styles, { layout } from "../../constants/styles";
//import Button from "../../components/Button";
import image from '../../constants/image';
import './home.css';

const Home = () => {
  return (
    <div className="home_app">
      <div className="app__background-img">
        <img src={image.Background} alt="bg" />
        <div className="layout-container">
          <section id="home" className={layout.section}>
            <div className={layout.sectionInfo}>
              <div className="entry-box">
                <div className="entry">
                  <div className={`${styles.paragraph} max-w-[470px] mt-5 entry`}>
                    <div className="word">Through</div>
                    <div className="word-details">
                      <div>Word Count = 7</div>
                      <div>Word Duration = 0.21secs</div>
                      <div>Homophone = Threw, Thru</div>
                    </div>
                  </div>
                  <div className={`${styles.paragraph} max-w-[470px] mt-5 entry`}>
                    <div className="word">Days</div>
                    <div className="word-details">
                      <div>Word Count = 4</div>
                      <div>Word Duration = 0.3secs</div>
                      <div>Homophone = Dais, Daise, Dase</div>
                    </div>
                  </div>
                  <div className={`${styles.paragraph} max-w-[470px] mt-5 entry`}>
                    <div className="word">Call</div>
                    <div className="word-details">
                      <div>Word Count = 4</div>
                      <div>Word Duration = 0.27secs</div>
                      <div>Homophone = Kall, Kaul</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Home;