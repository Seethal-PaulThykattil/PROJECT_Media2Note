import { useState, useRef } from 'react';
import './MainLayout.css';

const ScreenRecording = ({ onBack, onSave }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [snapshots, setSnapshots] = useState([]);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const snapshotIntervalRef = useRef(null);

  // Capture a still frame from the screen
  const captureSnapshot = () => {
    if (streamRef.current) {
      const canvas = document.createElement("canvas");
      const video = document.createElement("video");
      video.srcObject = streamRef.current;
      video.play();
      
      video.onloadedmetadata = () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageUrl = canvas.toDataURL("image/png");
        setSnapshots(prev => [...prev, imageUrl]);
      };
    }
  };

  const startRecording = async () => {
    try {
      // Request screen capture permission
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: {
          mediaSource: 'screen',
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: true
      });
      
      streamRef.current = stream;
      
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
      
      // Handle when user stops sharing screen
      stream.getVideoTracks()[0].onended = () => {
        stopRecording();
      };
      
    } catch (error) {
      console.error('Error accessing screen:', error);
      alert('Could not access screen. Please check permissions and try again.');
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
        name: `Screen Recording ${Date.now()}`,
        type: 'screen-recording',
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
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <h2>Screen Recording</h2>
      </div>
      
      <div className="screen-recording-container">
        <div className="recording-status">
          <div className={`recording-indicator ${isRecording ? 'active' : ''}`}>
            {isRecording ? '🔴 Recording Screen...' : '⏹️ Ready to Record Screen'}
          </div>
        </div>
        
        <div className="recording-controls">
          {!isRecording ? (
            <button className="record-btn start" onClick={startRecording}>
              🖥️ Start Screen Recording
            </button>
          ) : (
            <button className="record-btn stop" onClick={stopRecording}>
              ⏹️ Stop Screen Recording
            </button>
          )}
        </div>
        
        {recordedChunks.length > 0 && !isRecording && (
          <div className="recording-actions">
            <button className="action-btn save" onClick={saveRecording}>
              💾 Save Screen Recording
            </button>
            <button className="action-btn reset" onClick={resetRecording}>
              🔄 Record Again
            </button>
          </div>
        )}
        
        {snapshots.length > 0 && (
          <div className="snapshots-section">
            <h3>Captured Screenshots ({snapshots.length})</h3>
            <div className="snapshots-grid">
              {snapshots.map((snap, index) => (
                <img
                  key={index}
                  src={snap}
                  alt={`Screenshot ${index + 1}`}
                  className="snapshot"
                />
              ))}
            </div>
          </div>
        )}
        
        <div className="recording-info">
          <h3>Screen Recording Tips:</h3>
          <ul>
            <li>Choose which screen or application to record</li>
            <li>Ensure good screen resolution for quality</li>
            <li>Close unnecessary applications for better performance</li>
            <li>Screenshots are captured every 5 seconds automatically</li>
            <li>Click "Stop sharing" in browser to end recording</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ScreenRecording;
