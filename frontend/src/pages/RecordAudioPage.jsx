import { useNavigate } from 'react-router-dom';
import '../components/MainLayout.css';
import RecordAudio from '../components/RecordAudio';

const RecordAudioPage = () => {
  const navigate = useNavigate();

  return (
    <div className="page-container">
      <RecordAudio onBack={() => navigate('/')} />
    </div>
  );
};

export default RecordAudioPage;
