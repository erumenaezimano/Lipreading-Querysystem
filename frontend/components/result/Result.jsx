import React from 'react';
import { useLocation } from 'react-router-dom';
import Layout from '../layout/Layout';
import './result.css';

const Result = () => {
  const location = useLocation();
  const { state: searchResults } = location;

  return (
    <Layout>
      <div className="result-container">
        <h2>Search Results</h2>
        <div className="results-list">
          {searchResults && searchResults.criteria ? (
            <div className="result-item">
              <h3>Criteria: {searchResults.criteria}</h3>
              {renderResults(searchResults)}
            </div>
          ) : (
            <p>No results found for the selected criteria.</p>
          )}
        </div>
      </div>
    </Layout>
  );
};

const renderResults = (searchResults) => {

  const {
    criteria,
    homophone_results,
    visemes_results,
    phonemes_results,
    vowels_results,
    duration_results,
    negative_words_results,
  } = searchResults;


  if (criteria === 'Homophone' && homophone_results) {
    return (
      <div>
        {homophone_results.map((result, index) => (
          <div key={index} className="result-item">
            <p>Video ID: {result.video_id}</p>
            <p>Subtitle: {result.subtitle}</p>
            <p>Word: {result.word}</p>
            <p>Homophone: {result.homophones}</p>
            <p>Word Duration(sec): {result.duration}</p>
            <p>Video Duration(sec): {result.video_duration_sec}</p>
          </div>
        ))}
      </div>
    );
  } else if (criteria === 'Visemes' && visemes_results) {
    return (
      <div>
        {visemes_results.map((result, index) => (
          <div key={index} className="result-item">
            <p>Video ID: {result.video_id}</p>
            <p>Subtitle: {result.subtitle}</p>
            <p>Word: {result.word}</p>
            <p>Visemes: {result.visemes}</p>
            <p>Word Duration(sec): {result.duration_sec}</p>
            <p>Video Duration(sec): {result.video_duration_sec}</p>
          </div>
        ))}
      </div>
    );
  } else if (criteria === 'Phonemes' && phonemes_results) {
    return (
      <div>
        {phonemes_results.map((result, index) => (
          <div key={index} className="result-item">
            <p>Video ID: {result.video_id}</p>
            <p>Subtitle: {result.subtitle}</p>
            <p>Word: {result.word}</p>
            <p>Phoneme: {result.phonemes}</p>
            <p>Word Duration(sec): {result.duration_sec}</p>
            <p>Video Duration(sec): {result.video_duration_sec}</p>
          </div>
        ))}
      </div>
    );
  } else if (criteria === 'Vowels' && vowels_results) {
    return (
      <div>
        {vowels_results.map((result, index) => (
          <div key={index} className="result-item">
            <p>Video ID: {result.video_id}</p>
            <p>Subtitle: {result.subtitle}</p>
            <p>Word: {result.word}</p>
            <p>Vowel: {result.vowel}</p>
            <p>Word Duration(sec): {result.duration_sec}</p>
            <p>Video Duration(sec): {result.video_duration_sec}</p>
          </div>
        ))}
      </div>
    );
  } else if (criteria === 'Duration' && duration_results) {
    return (
      <div>
        {duration_results.map((result, index) => (
          <div key={index} className="result-item">
            <p>Video ID: {result.video_id}</p>
            <p>Subtitle: {result.subtitle}</p>
            <p>Word: {result.word}</p>
            <p>Word Duration(sec): {result.duration_sec}</p>
            <p>Word Speed: {result.word_speed}</p>
            <p>Video Duration(sec): {result.video_duration_sec}</p>
          </div>
        ))}
      </div>
    );
  } else if (criteria === 'Negative Words' && negative_words_results) {
    return (
      <div>
        {negative_words_results.map((result, index) => (
          <div key={index} className="result-item">
            <p>Video ID: {result.video_id}</p>
            <p>Subtitle: {result.subtitle}</p>
            <p>Negative Word: {result.word}</p>
            <p>Video Duration(sec): {result.video_duration_sec}</p>
          </div>
        ))}
      </div>
    );
  } else {
    return <p>No results found for the selected criteria.</p>;
  }
};

export default Result;