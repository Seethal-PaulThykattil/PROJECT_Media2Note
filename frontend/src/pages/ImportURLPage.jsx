import { useNavigate } from 'react-router-dom';
import '../components/MainLayout.css';
import ImportURL from '../components/ImportURL';

const ImportURLPage = () => {
  const navigate = useNavigate();

  return (
    <div className="page-container">
      <ImportURL onBack={() => navigate('/')} />
    </div>
  );
};

export default ImportURLPage;
