import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import MainDashboard from './components/MainDashboard';
import Assessment from './components/Assessment';
import Report from './components/Report';

function App() {
  return (
    <Router>
      <div className="min-h-screen font-sans bg-[var(--color-pearl)] text-[var(--color-dark)]">
        <header className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-royal to-sky-400 tracking-tight flex items-center gap-2">
              <svg className="w-8 h-8 text-royal" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
              Carrier Guider
            </h1>
          </div>
        </header>
        <main className="p-4 sm:p-6 lg:p-8 relative">
          {/* Subtle global background decoration */}
          <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 rounded-full bg-blue-50 blur-3xl opacity-50 pointer-events-none"></div>
          <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-72 h-72 rounded-full bg-indigo-50 blur-3xl opacity-50 pointer-events-none"></div>
          
          <div className="relative z-10">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/main" element={<MainDashboard />} />
              <Route path="/assessment" element={<Assessment />} />
              <Route path="/report" element={<Report />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
