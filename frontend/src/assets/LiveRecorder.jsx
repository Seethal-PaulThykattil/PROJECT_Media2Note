import React, { useRef, useState } from 'react';

function LiveRecorder() {
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const snapshotIntervalRef = useRef(null);

  const [recordedChunks, setRecordedChunks] = useState([]);
  const [recording, setRecording] = useState(false);
  const [error, setError] = useState(null);
  const [snapshots, setSnapshots] = useState([]);

  // Capture a still frame from the webcam
  const captureSnapshot = () => {
    if (videoRef.current) {
      const canvas = document.createElement("canvas");
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
      const imageUrl = canvas.toDataURL("image/png");
      setSnapshots((prev) => [...prev, imageUrl]);
    }
  };

  // Start recording and snapshots
  const startRecording = async () => {
    try {
      setError(null);
      setSnapshots([]); // clear old snapshots
      setRecordedChunks([]); // clear old recordings

      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });

      videoRef.current.srcObject = stream;

      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setRecordedChunks((prev) => [...prev, event.data]);
        }
      };

      mediaRecorderRef.current.start();

      // take snapshot every 5 seconds
      snapshotIntervalRef.current = setInterval(captureSnapshot, 5000);

      setRecording(true);
    } catch (err) {
      console.error("Error accessing media devices:", err);
      setError("⚠️ Unable to access webcam/microphone. Please check permissions.");
    }
  };

  // Stop recording and snapshots
  const stopRecording = () => {
    mediaRecorderRef.current.stop();

    const stream = videoRef.current.srcObject;
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }

    if (snapshotIntervalRef.current) {
      clearInterval(snapshotIntervalRef.current);
    }

    setRecording(false);
  };

  // Download recorded video
  const downloadRecording = () => {
    const blob = new Blob(recordedChunks, { type: "video/webm" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "recording.webm";
    a.click();
  };

  return (
    <div style={{ textAlign: "center", padding: "2rem" }}>
      <h2>Live Session Recorder</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <video
        ref={videoRef}
        autoPlay
        playsInline
        style={{ width: "60%", borderRadius: "10px", marginBottom: "1rem" }}
      />
      <br/>

      {!recording ? (
        <button
          onClick={startRecording}
          style={{
            backgroundColor: "#007bff",
            color: "white",
            padding: "14px 26px",
            border: "none",
            borderRadius: "10px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Start Recording
        </button>
      ) : (
        <button
          onClick={stopRecording}
          style={{
            backgroundColor: "#dc3545",
            color: "white",
            padding: "14px 26px",
            border: "none",
            borderRadius: "10px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Stop Recording
        </button>
      )}

      <br />
      <br />

      {recordedChunks.length > 0 && (
        <button
          onClick={downloadRecording}
          style={{
            backgroundColor: "#28a745",
            color: "white",
            padding: "14px 26px",
            border: "none",
            borderRadius: "10px",
            fontSize: "16px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Download Recording
        </button>
      )}

      {snapshots.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Captured Stills</h3>
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              justifyContent: "center",
            }}
          >
            {snapshots.map((snap, index) => (
              <img
                key={index}
                src={snap}
                alt={`Snapshot ${index}`}
                style={{
                  width: "150px",
                  margin: "5px",
                  borderRadius: "8px",
                  border: "1px solid #ccc",
                }}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default LiveRecorder;
