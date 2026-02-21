import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const MainDashboard = () => {
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get('/main');
        if (res.data.success) {
          setUserData(res.data);
        }
      } catch (err) {
        navigate('/');
      }
    };
    fetchUser();
  }, [navigate]);

  const handleLogout = async () => {
    try {
      await api.get('/logout');
      navigate('/');
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  const startAssessment = () => {
    navigate('/assessment');
  };

  if (!userData) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-royal"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto mt-12 bg-white rounded-2xl shadow-xl overflow-hidden">
      <div className="bg-gradient-to-r from-royal to-royal-dark p-8 text-white relative">
        <button 
          onClick={handleLogout}
          className="absolute top-4 right-4 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition backdrop-blur-sm"
        >
          Logout
        </button>
        <h2 className="text-3xl font-bold mb-2">Welcome, {userData.name}!</h2>
        <p className="text-blue-100 flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l9-5-9-5-9 5 9 5z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path></svg>
          Education Profile: <span className="font-semibold">{userData.education}</span>
        </p>
      </div>
      
      <div className="p-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-6">Your Next Steps</h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="border border-gray-100 p-6 rounded-xl bg-gray-50 hover:bg-white hover:shadow-md transition cursor-pointer group" onClick={startAssessment}>
            <div className="w-12 h-12 bg-blue-100 text-royal rounded-full flex items-center justify-center mb-4 group-hover:bg-royal group-hover:text-white transition">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
            </div>
            <h4 className="text-lg font-bold text-gray-900 mb-2">Take New Assessment</h4>
            <p className="text-gray-600">Analyze your academic strengths, personality, and interests to get a tailored career roadmap.</p>
          </div>
          
          <div className="border border-gray-100 p-6 rounded-xl bg-gray-50 hover:bg-white hover:shadow-md transition cursor-pointer group" onClick={() => navigate('/report')}>
            <div className="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-4 group-hover:bg-green-600 group-hover:text-white transition">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </div>
            <h4 className="text-lg font-bold text-gray-900 mb-2">View Previous Roadmap</h4>
            <p className="text-gray-600">Check out your most recent AI-generated career roadmap and recommendations.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainDashboard;
