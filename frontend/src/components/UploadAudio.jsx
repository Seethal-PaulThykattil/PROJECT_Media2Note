import { useNavigate } from 'react-router-dom';
import './MainLayout.css';

const UploadAudio = () => {
  const navigate = useNavigate();

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Selected file:', file);
      // You can now upload the file or handle it as needed.
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate('/')}>← Back</button>
        <h2>Upload Audio</h2>
      </div>
      <div className="upload-container">
        <input type="file" accept="audio/*" onChange={handleFileSelect} />
      </div>
    </div>
  );
};

export default UploadAudio;
