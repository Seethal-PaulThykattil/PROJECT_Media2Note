import { useState, useRef } from 'react';
import './MainLayout.css';

const RecordAudio = ({ onBack, onSave }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setRecordedChunks(prev => [...prev, event.data]);
        }
      };
      
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
    
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    
    setIsRecording(false);
  };

  const saveRecording = () => {
    if (recordedChunks.length > 0) {
      const blob = new Blob(recordedChunks, { type: 'audio/wav' });
      const newRecording = {
        id: Date.now(),
        name: `Audio Recording ${Date.now()}`,
        type: 'audio-recording',
        blob: blob,
        timestamp: new Date().toISOString()
      };
      onSave(newRecording);
      onBack();
    }
  };

  const resetRecording = () => {
    setRecordedChunks([]);
    setIsRecording(false);
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <h2>Record Audio</h2>
      </div>
      
      <div className="recording-container">
        <div className="recording-status">
          <div className={`recording-indicator ${isRecording ? 'active' : ''}`}>
            {isRecording ? '🔴 Recording...' : '⏹️ Ready to Record'}
          </div>
        </div>
        
        <div className="recording-controls">
          {!isRecording ? (
            <button className="record-btn start" onClick={startRecording}>
              🎤 Start Recording
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
              💾 Save Recording
            </button>
            <button className="action-btn reset" onClick={resetRecording}>
              🔄 Record Again
            </button>
          </div>
        )}
        
        <div className="recording-info">
          <h3>Recording Tips:</h3>
          <ul>
            <li>Ensure your microphone is working properly</li>
            <li>Speak clearly and at a normal volume</li>
            <li>Minimize background noise</li>
            <li>Click "Stop Recording" when finished</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default RecordAudio;
