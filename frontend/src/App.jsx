import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LiveSession from './components/LiveSession';
import UploadVideo from './components/UploadVideo';
import UploadAudio from './components/UploadAudio';
import UploadDocument from './components/UploadDocument';
import ImportURLPage from './pages/ImportURLPage';
import RecordAudioPage from './pages/RecordAudioPage';
import ScreenRecordingPage from './pages/ScreenRecordingPage';
import Notes from './assets/Notes';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/live-session" element={<LiveSession />} />
      <Route path="/upload-video" element={<UploadVideo />} />
      <Route path="/upload-audio" element={<UploadAudio />} />
      <Route path="/upload-document" element={<UploadDocument />} />
      <Route path="/import-url" element={<ImportURLPage />} />
      <Route path="/record-audio" element={<RecordAudioPage />} />
      <Route path="/screen-recording" element={<ScreenRecordingPage />} />
      <Route path="/notes" element={<Notes />} />
    </Routes>
  );
}

export default App;
