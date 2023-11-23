import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Layout from '../layout/Layout';
import baseUrl from '../../config';
import './search.css';


const Search = () => {

  const [criteria, setCriteria] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (criteria && query) {
          const responseGet = await axios.get(`${baseUrl}/search?criteria=${criteria}&user_input=${query}`, {
            params: {
              criteria: criteria,
              user_input: query,
            },
          });
          console.log("GET API response:", responseGet.data,criteria);
          setResults(responseGet.data[criteria] || [] );
        }
      } catch (error) {
        console.error('GET API error:', error);
      }
    };

    fetchData(); // Call fetchData inside useEffect

  }, [criteria, query]);


  const handleSearch = async (event) => {
    event.preventDefault();
    if (criteria && query) {
      try {
        const postData = {
          criteria: criteria,
          user_input: query,
        };
        console.log('POST Data:', postData);
  
        const responsePost = await axios.post(`${baseUrl}/search`, postData);
        console.log('POST API response:', responsePost.data);
  
        setResults(responsePost.data[criteria] || []);
      } catch (error) {
        console.error('POST API error:', error);
      }
    }
  };


  return (
    <Layout>

      <div className="search-container">
        <div className="search-input">
          <form className="form-inline" onSubmit={handleSearch}>
            <select className="form-control" name="criteria" value={criteria} onChange={e => setCriteria(e.target.value)}>
              <option value="">Select Criteria</option>
              <option value="Homophone">Homophone</option>
              <option value="Visemes">Visemes</option>
              <option value="Phonemes">Phonemes</option>
              <option value="Duration">Duration</option>
              <option value="Vowels">Vowels</option>
              <option value="Negative Words">Negative Words</option>
            </select>
            <input type="text" className="form-control" name="query" placeholder="Search word" value={query} onChange={e => setQuery(e.target.value)} />
            <button className="btn btn-outline-success" type="submit">
              Search
            </button>
          </form>
          <p>Search Results: {results.length}</p>
        </div>
      </div>
      <div className="results"> 
      {results.length > 0 && (
          <div>
            {results?.map((result, index) => (
              <div key={index} className="result-item">
                <div className="result">
                  <h3>{criteria}</h3>
                  <p>Video ID: {result.video_id}</p>
                  <p>Subtitle: {result.subtitle}</p>
                  <p>Word: {result.word}</p>
                  {criteria === 'Homophone' && <p>Homophones: {result.homophones}</p>}
                  {criteria === 'Visemes' && <p>Visemes: {result.visemes}</p>}
                  {criteria === 'Phonemes' && <p>Phonemes: {result.phonemes}</p>}
                  {criteria === 'Vowels' && <p>Vowels: {result.vowel}</p>}
                  {/* {criteria === 'Duration' && <p>Duration: {result.word_speed}</p>} */}
                  <p>Word Duration(sec): {result.duration_sec}</p>
                  <p>Video Duration(sec): {result.video_duration_sec}</p>
                </div>
              </div>
            ))}
            </div>
          )}
        </div>
      </Layout>
    );
  };
  
  export default Search;