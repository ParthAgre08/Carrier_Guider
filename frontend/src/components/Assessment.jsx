import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const questions = [
  { id: 'q1_r', text: 'I like repairing things or working with tools.', category: 'R' },
  { id: 'q1_i', text: 'I enjoy solving complex math or science problems.', category: 'I' },
  { id: 'q1_a', text: 'I enjoy writing stories, poetry, or making art.', category: 'A' },
  { id: 'q1_s', text: 'I like helping people solve their personal problems.', category: 'S' },
  { id: 'q1_e', text: 'I like leading teams and managing projects.', category: 'E' },
  { id: 'q1_c', text: 'I like organizing files, data, and schedules.', category: 'C' }
];

const Assessment = () => {
  const [step, setStep] = useState(1);
  const [education, setEducation] = useState('Grade 10');
  const [academicData, setAcademicData] = useState({});
  const [personalityData, setPersonalityData] = useState({});
  const [interestData, setInterestData] = useState({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch user education to render appropriate form
    const fetchUser = async () => {
      try {
        const res = await api.get('/main');
        if (res.data.success) {
          setEducation(res.data.education);
        }
      } catch (err) {
        navigate('/');
      }
    };
    fetchUser();
  }, [navigate]);

  const handleAcademicChange = (e) => setAcademicData({ ...academicData, [e.target.name]: e.target.value });
  const handlePersonalityChange = (id, value) => setPersonalityData({ ...personalityData, [id]: value });
  const handleInterestChange = (e) => setInterestData({ ...interestData, [e.target.name]: e.target.value });

  const submitAcademic = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/assessment', academicData);
      setStep(2);
    } catch (err) {
      alert('Error submitting academic data');
    }
    setLoading(false);
  };

  const submitPersonality = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/personality_assessment', personalityData);
      setStep(3);
    } catch (err) {
      alert('Error submitting personality data');
    }
    setLoading(false);
  };

  const submitInterest = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/interest_assessment', interestData);
      // Immediately trigger generation after interest submission
      const profileRes = await api.get('/generate_career_profile');
      if (profileRes.data.success) {
        navigate('/report');
      }
    } catch (err) {
      alert('Error finalizing assessment');
    }
    setLoading(false);
  };

  // Dynamic Bar Components
  const DynamicBarSlider = ({ value, onChange, labelLeft = 'Strongly Disagree', labelRight = 'Strongly Agree' }) => {
    // Calculate width: value from 1 to 5 corresponds to 0% to 100%
    const normalizedValue = value ? parseInt(value) : 3;
    const percentage = ((normalizedValue - 1) / 4) * 100;

    return (
      <div className="mt-4">
        <div className="flex justify-between text-xs font-semibold text-gray-500 mb-2 px-1">
          <span>{labelLeft} (1)</span>
          <span>Neutral (3)</span>
          <span>{labelRight} (5)</span>
        </div>
        <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-royal to-sky-400 transition-all duration-300 ease-out"
            style={{ width: `${percentage}%` }}
          />
        </div>
        <input 
          type="range" 
          min="1" 
          max="5" 
          value={normalizedValue} 
          onChange={(e) => onChange(e.target.value)}
          className="w-full mt-2 cursor-pointer accent-royal"
        />
        <div className="text-center mt-2 text-sm font-bold text-royal">
          Score: {normalizedValue} - {normalizedValue === 1 ? 'Strongly Disagree' : normalizedValue === 2 ? 'Disagree' : normalizedValue === 3 ? 'Neutral' : normalizedValue === 4 ? 'Agree' : 'Strongly Agree'}
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-3xl mx-auto mt-8 bg-white rounded-2xl shadow-xl overflow-hidden p-8">
      {/* Progress Indicator */}
      <div className="flex justify-between mb-8 relative">
        <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-200 -z-10 transform -translate-y-1/2 rounded"></div>
        <div className="absolute top-1/2 left-0 h-1 bg-royal -z-10 transform -translate-y-1/2 rounded transition-all duration-500" style={{ width: `${((step - 1) / 2) * 100}%` }}></div>
        
        {['Academic', 'Personality', 'Interests'].map((label, idx) => (
          <div key={label} className="flex flex-col items-center">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-colors duration-300 ${step > idx + 1 ? 'bg-royal text-white' : step === idx + 1 ? 'bg-royal text-white shadow-[0_0_15px_rgba(37,99,235,0.4)]' : 'bg-gray-200 text-gray-400'}`}>
              {idx + 1}
            </div>
            <span className={`mt-2 text-xs font-semibold ${step >= idx + 1 ? 'text-royal' : 'text-gray-400'}`}>{label}</span>
          </div>
        ))}
      </div>

      {step === 1 && (
        <form onSubmit={submitAcademic} className="animate-fade-in">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Academic Assessment</h2>
          <p className="text-center text-gray-600 mb-6 font-medium bg-blue-50 py-2 rounded-lg">Profile: {education}</p>
          
          <div className="space-y-4">
            {education === 'Grade 10' ? (
              <>
                {['English', 'Math', 'Science', 'SocialScience', 'SecondLanguage'].map(subject => (
                  <div key={subject}>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">{subject} Score (%)</label>
                    <input type="number" min="0" max="100" name={subject.toLowerCase()} onChange={handleAcademicChange} required className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-royal outline-none" placeholder="e.g. 85" />
                  </div>
                ))}
              </>
            ) : (
              <>
                <p className="text-sm text-gray-500 italic mb-4">Please input your major subject scores.</p>
                {['English', 'Mathematics', 'Physics', 'Chemistry', 'Biology'].map(subject => (
                  <div key={subject}>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">{subject} Score (%)</label>
                    <input type="number" min="0" max="100" name={subject.toLowerCase()} onChange={handleAcademicChange} className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-royal outline-none" placeholder="e.g. 85" />
                  </div>
                ))}
              </>
            )}
          </div>
          <button disabled={loading} type="submit" className="w-full mt-8 bg-royal hover:bg-royal-dark text-white font-bold py-4 rounded-xl shadow-lg transition disabled:opacity-70">
            {loading ? 'Saving...' : 'Next: Personality Test →'}
          </button>
        </form>
      )}

      {step === 2 && (
        <form onSubmit={submitPersonality} className="animate-fade-in">
          <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">Personality Assessment</h2>
          <p className="text-gray-600 text-center mb-8">Rate how much you agree with the following statements.</p>
          
          <div className="space-y-10">
            {questions.map((q) => (
              <div key={q.id} className="p-6 bg-gray-50 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
                <p className="font-semibold text-lg text-gray-800 tracking-tight">{q.text}</p>
                <DynamicBarSlider 
                  value={personalityData[q.id]} 
                  onChange={(val) => handlePersonalityChange(q.id, val)}
                />
              </div>
            ))}
          </div>

          <div className="flex gap-4 mt-8">
            <button type="button" onClick={() => setStep(1)} className="w-1/3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 rounded-xl transition">
              ← Back
            </button>
            <button disabled={loading} type="submit" className="w-2/3 bg-royal hover:bg-royal-dark text-white font-bold py-4 rounded-xl shadow-lg transition">
              {loading ? 'Saving...' : 'Next: Interests →'}
            </button>
          </div>
        </form>
      )}

      {step === 3 && (
        <form onSubmit={submitInterest} className="animate-fade-in">
          <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">Your Interests</h2>
          <p className="text-gray-600 text-center mb-8">Rate your interest level in the following fields.</p>
          
          <div className="space-y-10">
            {[
              { id: 'interest_math', label: 'Mathematics & Logic' },
              { id: 'interest_science', label: 'Science & Nature' },
              { id: 'interest_business', label: 'Business & Finance' },
              { id: 'interest_creative', label: 'Arts & Creativity' },
              { id: 'interest_social', label: 'Social & Helping Others' }
            ].map(field => (
              <div key={field.id} className="p-6 bg-gray-50 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
                <p className="font-semibold text-lg text-gray-800 tracking-tight">{field.label}</p>
                <DynamicBarSlider 
                  value={interestData[field.id]} 
                  onChange={(val) => setInterestData({ ...interestData, [field.id]: val })}
                  labelLeft="No Interest"
                  labelRight="High Interest"
                />
              </div>
            ))}
          </div>

          <div className="flex gap-4 mt-8">
            <button type="button" onClick={() => setStep(2)} className="w-1/3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 rounded-xl transition">
              ← Back
            </button>
            <button disabled={loading} type="submit" className="w-2/3 bg-green-600 hover:bg-green-700 text-white font-bold py-4 rounded-xl shadow-lg transition flex items-center justify-center gap-2">
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Generating AI Analysis...
                </>
              ) : 'Generate Career Profile ✨'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default Assessment;
