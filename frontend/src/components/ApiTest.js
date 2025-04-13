import React, { useState } from 'react';
import axios from 'axios';

const ApiTest = () => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('python');
  const [selectedPlatforms, setSelectedPlatforms] = useState({
    reddit: true,
    hackernews: false,
    quora: false
  });

  const handlePlatformChange = (platform) => {
    setSelectedPlatforms({
      ...selectedPlatforms,
      [platform]: !selectedPlatforms[platform]
    });
  };

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Get selected platforms as array
      const platforms = Object.keys(selectedPlatforms).filter(key => selectedPlatforms[key]);
      
      if (platforms.length === 0) {
        throw new Error('Please select at least one platform');
      }

      const response = await axios.post('/api/search', {
        project: searchTerm,
        platforms: platforms,
        num_posts: 5
      });

      setResponse(response.data);
      console.log('API Response:', response.data);
    } catch (err) {
      setError(err.message || 'An error occurred while fetching data');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>API Connection Test</h2>
      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="searchTerm" style={{ display: 'block', marginBottom: '5px' }}>
          Search Term:
        </label>
        <input
          id="searchTerm"
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ padding: '8px', width: '100%', marginBottom: '10px' }}
        />
        
        <div style={{ marginBottom: '10px' }}>
          <p style={{ marginBottom: '5px' }}>Select Platforms:</p>
          <div style={{ display: 'flex', gap: '10px' }}>
            <label>
              <input
                type="checkbox"
                checked={selectedPlatforms.reddit}
                onChange={() => handlePlatformChange('reddit')}
              />
              Reddit
            </label>
            <label>
              <input
                type="checkbox"
                checked={selectedPlatforms.hackernews}
                onChange={() => handlePlatformChange('hackernews')}
              />
              Hacker News
            </label>
            <label>
              <input
                type="checkbox"
                checked={selectedPlatforms.quora}
                onChange={() => handlePlatformChange('quora')}
              />
              Quora
            </label>
          </div>
        </div>
        
        <button
          onClick={handleSearch}
          disabled={loading}
          style={{
            padding: '10px 15px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Loading...' : 'Test API Connection'}
        </button>
      </div>

      {error && (
        <div style={{ padding: '15px', backgroundColor: '#ffebee', color: '#c62828', borderRadius: '4px', marginBottom: '20px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {response && (
        <div>
          <h3>API Response:</h3>
          <div style={{ padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '4px', overflowX: 'auto' }}>
            <h4>Project: {response.project}</h4>
            
            <h4>Overall Sentiment:</h4>
            <ul>
              <li>Positive: {response.overall_sentiment.positive_percentage.toFixed(2)}%</li>
              <li>Neutral: {response.overall_sentiment.neutral_percentage.toFixed(2)}%</li>
              <li>Negative: {response.overall_sentiment.negative_percentage.toFixed(2)}%</li>
            </ul>
            
            <h4>Top Keywords:</h4>
            <ul>
              {response.top_keywords.map((item, index) => (
                <li key={index}>{item.keyword}: {item.count}</li>
              ))}
            </ul>
            
            <h4>Results Count: {response.results.length}</h4>
            {response.results.length > 0 && (
              <div>
                <h4>Sample Result:</h4>
                <p><strong>Platform:</strong> {response.results[0].platform}</p>
                <p><strong>Title:</strong> {response.results[0].title}</p>
                <p><strong>Sentiment:</strong> {response.results[0].sentiment}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ApiTest;
