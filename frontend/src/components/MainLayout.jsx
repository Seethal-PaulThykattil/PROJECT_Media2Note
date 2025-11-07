import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ImportURL from './ImportURL';
import RecordAudio from './RecordAudio';
import ScreenRecording from './ScreenRecording';
import './MainLayout.css';

const MainLayout = () => {
  const [activeTab, setActiveTab] = useState('home');
  const [showModal, setShowModal] = useState(false);
  const [recordings, setRecordings] = useState([]);
  const navigate = useNavigate();

  const handleRecordLiveSession = () => {
    navigate('/live-session');
  };

  const handleImportURL = () => {
    navigate('/import-url');
  };

  const handleUploadVideo = () => {
    navigate('/upload-video');
  };

  const handleRecordAudio = () => {
    navigate('/record-audio');
  };

  const handleUploadAudio = () => {
    navigate('/upload-audio');
  };

  const handleUploadDocument = () => {
    navigate('/upload-document');
  };

  const handleScreenRecording = () => {
    navigate('/screen-recording');
  };

  return (
    <div className="app-container">
      {/* Left Sidebar */}
      <div className="sidebar">
        <div className="logo-section">
          <div className="logo-icon">
            <span className="logo-m">M</span>
          </div>
          <span className="logo-text">Media 2 Note</span>
        </div>

        <div className="nav-section">
          <div className="nav-item active" onClick={() => setActiveTab('home')}>
            <span className="nav-icon">🏠</span>
            <span className="nav-text">Home</span>
          </div>
          <div className="nav-item" onClick={() => setActiveTab('recordings')}>
            <span className="nav-icon">📁</span>
            <span className="nav-text">My Recordings</span>
          </div>
          <div className="nav-item" onClick={() => setActiveTab('meetings')}>
            <span className="nav-icon">📅</span>
            <span className="nav-text">My Meetings</span>
          </div>
        </div>

        <div className="nav-section">
          <div className="section-header">
            <span>FOLDERS</span>
            <span className="add-icon">+</span>
          </div>
        </div>

        <div className="nav-section">
          <div className="section-header">
            <span>OTHER</span>
          </div>
          <div className="nav-item">
            <span className="nav-icon">🕒</span>
            <span className="nav-text">History</span>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="main-content">
        {/* Header */}
        <div className="header">
          <div className="header-left">
            <div className="header-logo">
              <span className="logo-m">M</span>
            </div>
            <span className="header-text">Media 2 Note</span>
          </div>
          <div className="header-right">
            <div className="user-avatar">👤</div>
          </div>
        </div>

        {/* Quick Action Buttons */}
        <div className="quick-actions">
          <div className="action-card purple" onClick={handleRecordLiveSession}>
            <div className="action-icon">📹</div>
            <div className="action-content">
              <h3>Record Live Session</h3>
              <p>Camera & microphone</p>
            </div>
          </div>
          <div className="action-card teal" onClick={handleImportURL}>
            <div className="action-icon">🔗</div>
            <div className="action-content">
              <h3>Import URL</h3>
              <p>Enter video URL</p>
            </div>
          </div>
          <div className="action-card orange" onClick={handleUploadVideo}>
            <div className="action-icon">📹</div>
            <div className="action-content">
              <h3>Upload Video</h3>
              <p>Select video file</p>
            </div>
          </div>
          <div className="action-card dark-purple" onClick={handleRecordAudio}>
            <div className="action-icon">🎤</div>
            <div className="action-content">
              <h3>Record Audio</h3>
              <p>Microphone recording</p>
            </div>
          </div>
          <div className="action-card green" onClick={handleUploadAudio}>
            <div className="action-icon">🎵</div>
            <div className="action-content">
              <h3>Upload Audio</h3>
              <p>Select audio file</p>
            </div>
          </div>
          <div className="action-card blue" onClick={handleUploadDocument}>
            <div className="action-icon">📄</div>
            <div className="action-content">
              <h3>Upload Document</h3>
              <p>Select document file</p>
            </div>
          </div>
          <div className="action-card red" onClick={handleScreenRecording}>
            <div className="action-icon">🖥️</div>
            <div className="action-content">
              <h3>Screen Recording</h3>
              <p>Record your screen</p>
            </div>
          </div>
        </div>

        {/* Content Area */}
        {recordings.length === 0 ? (
          <div className="empty-state">
            <h2>Add your first recording</h2>
            <p>Upload files, import URLs, or record audio and screen directly. We'll create transcripts and summaries to help you quickly find what you need.</p>
          </div>
        ) : (
          <div className="recordings-list">
            <h2>Your Recordings ({recordings.length})</h2>
            <div className="recordings-grid">
              {recordings.map((recording) => (
                <div key={recording.id} className="recording-card">
                  <div className="recording-icon">
                    {recording.type === 'microphone' && '🎤'}
                    {recording.type === 'upload' && '📁'}
                    {recording.type === 'dictation' && '📝'}
                  </div>
                  <div className="recording-info">
                    <h3>{recording.name}</h3>
                    <p>{new Date(recording.timestamp).toLocaleDateString()}</p>
                    <span className="recording-type">{recording.type}</span>
                  </div>
                  <div className="recording-actions">
                    <button className="action-btn">📄</button>
                    <button className="action-btn">📝</button>
                    <button className="action-btn">🗑️</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Modal for Authentication */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-logo">
              <span className="logo-m">M</span>
            </div>
            <h2>Welcome to Media 2 Note</h2>
            <button className="google-btn">
              <span className="google-icon">G</span>
              Continue with Google
            </button>
            <button className="apple-btn">
              <span className="apple-icon">🍎</span>
              Continue with Apple
            </button>
            <div className="or-divider">or</div>
            <input type="email" placeholder="Email Address" className="email-input" />
            <div className="modal-footer">
              <span>Already have an account? <a href="#">Sign in</a></span>
              <span>By using Media 2 Note you agree to the <a href="#">Terms</a></span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MainLayout;
