import { useState, useRef } from 'react';
import './MainLayout.css';

const LiveSession = ({ onBack, onSave }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [snapshots, setSnapshots] = useState([]);
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const snapshotIntervalRef = useRef(null);
  const streamRef = useRef(null);

  const captureSnapshot = () => {
    if (videoRef.current) {
      const canvas = document.createElement("canvas");
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
      const imageUrl = canvas.toDataURL("image/png");
      setSnapshots(prev => [...prev, imageUrl]);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });
      
      streamRef.current = stream;
      videoRef.current.srcObject = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setRecordedChunks(prev => [...prev, event.data]);
        }
      };
      
      mediaRecorder.start();
      
      // Take snapshot every 5 seconds
      snapshotIntervalRef.current = setInterval(captureSnapshot, 5000);
      
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing media devices:', error);
      alert('Could not access camera/microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
    
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    
    if (snapshotIntervalRef.current) {
      clearInterval(snapshotIntervalRef.current);
    }
    
    setIsRecording(false);
  };

  const saveRecording = () => {
    if (recordedChunks.length > 0) {
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      const newRecording = {
        id: Date.now(),
        name: `Live Session ${Date.now()}`,
        type: 'live-session',
        blob: blob,
        snapshots: snapshots,
        timestamp: new Date().toISOString()
      };
      onSave(newRecording);
      onBack();
    }
  };

  const resetRecording = () => {
    setRecordedChunks([]);
    setSnapshots([]);
    setIsRecording(false);
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <h2>Record Live Session</h2>
      </div>
      
      <div className="live-session-container">
        <div className="video-container">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="live-video"
          />
          <div className={`recording-overlay ${isRecording ? 'active' : ''}`}>
            {isRecording ? '🔴 LIVE' : '⏹️ Ready'}
          </div>
        </div>
        
        <div className="recording-controls">
          {!isRecording ? (
            <button className="record-btn start" onClick={startRecording}>
              📹 Start Recording
            </button>
          ) : (
            <button className="record-btn stop" onClick={stopRecording}>
              ⏹️ Stop Recording
            </button>
          )}
        </div>
        
        {recordedChunks.length > 0 && !isRecording && (
          <div className="recording-actions">
            <button className="action-btn save" onClick={saveRecording}>
              💾 Save Session
            </button>
            <button className="action-btn reset" onClick={resetRecording}>
              🔄 Record Again
            </button>
          </div>
        )}
        
        {snapshots.length > 0 && (
          <div className="snapshots-section">
            <h3>Captured Moments ({snapshots.length})</h3>
            <div className="snapshots-grid">
              {snapshots.map((snap, index) => (
                <img
                  key={index}
                  src={snap}
                  alt={`Snapshot ${index + 1}`}
                  className="snapshot"
                />
              ))}
            </div>
          </div>
        )}
        
        <div className="recording-info">
          <h3>Live Session Tips:</h3>
          <ul>
            <li>Ensure good lighting for video quality</li>
            <li>Check camera and microphone permissions</li>
            <li>Speak clearly and maintain eye contact</li>
            <li>Snapshots are captured every 5 seconds</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default LiveSession;
