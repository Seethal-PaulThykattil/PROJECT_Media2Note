import { useNavigate } from 'react-router-dom';
import '../components/MainLayout.css';
import ScreenRecording from '../components/ScreenRecording';

const ScreenRecordingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="page-container">
      <ScreenRecording onBack={() => navigate('/')} />
    </div>
  );
};

export default ScreenRecordingPage;
