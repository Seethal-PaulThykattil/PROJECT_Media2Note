import { useState } from 'react';
import './MainLayout.css';

const ImportURL = ({ onBack, onImport }) => {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;

    setIsLoading(true);
    
    // Simulate processing
    setTimeout(() => {
      const newRecording = {
        id: Date.now(),
        name: `URL Import - ${url}`,
        type: 'url',
        url: url,
        timestamp: new Date().toISOString()
      };
      onImport(newRecording);
      setIsLoading(false);
      onBack();
    }, 2000);
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <h2>Import URL</h2>
      </div>
      
      <div className="url-form-container">
        <form onSubmit={handleSubmit} className="url-form">
          <div className="input-group">
            <label htmlFor="url-input">Enter Video URL</label>
            <input
              id="url-input"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/video.mp4"
              required
              className="url-input"
            />
          </div>
          
          <button 
            type="submit" 
            className="import-btn"
            disabled={isLoading || !url.trim()}
          >
            {isLoading ? 'Processing...' : 'Import URL'}
          </button>
        </form>
        
        <div className="url-help">
          <h3>Supported URLs:</h3>
          <ul>
            <li>Direct video links (.mp4, .webm, .mov)</li>
            <li>YouTube videos</li>
            <li>Vimeo videos</li>
            <li>Other streaming platforms</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ImportURL;
