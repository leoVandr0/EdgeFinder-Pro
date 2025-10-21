import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Strength from './pages/Strength';
import Events from './pages/Events';
import Compare from './pages/Compare';
import Insights from './pages/Insights';
import News from './pages/News';
import PWAInstallPrompt from './components/PWAInstallPrompt';
import OfflineIndicator from './components/OfflineIndicator';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <OfflineIndicator />
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/strength" element={<Strength />} />
            <Route path="/events" element={<Events />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/insights" element={<Insights />} />
            <Route path="/news" element={<News />} />
          </Routes>
        </main>
        <PWAInstallPrompt />
      </div>
    </Router>
  );
}

export default App;
