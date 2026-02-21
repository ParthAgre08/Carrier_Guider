import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Home = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ name: '', email: '', password: '', education: 'Grade 10' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      if (isLogin) {
        const res = await api.post('/login', { email: formData.email, password: formData.password });
        if (res.data.success) {
          navigate('/main');
        }
      } else {
        const res = await api.post('/register', formData);
        if (res.data.success) {
          navigate('/main');
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during authentication.');
    }
  };

  return (
    <div className="flex flex-col md:flex-row gap-8 items-center justify-center min-h-[80vh]">
      {/* Description Card */}
      <div className="md:w-1/2 p-8 bg-white/80 backdrop-blur-md rounded-2xl shadow-xl border border-gray-100 transform transition-all hover:scale-[1.02]">
        <h2 className="text-3xl font-bold text-royal mb-4">Carrier Guider Prototype</h2>
        <p className="text-gray-700 text-lg leading-relaxed mb-4">
          Welcome to the Carrier Guider. This prototype leverages advanced machine learning algorithms and deep psychometric analysis to help students determine the optimal academic stream and career path.
        </p>
        <p className="text-gray-600">
          By evaluating your academic scores, RIASEC personality traits, and personal interests, our AI engine generates a highly personalized roadmap tailored just for you. Get started by registering or logging in to take the assessment!
        </p>
      </div>

      {/* Auth Card */}
      <div className="md:w-1/3 w-full bg-white p-8 rounded-2xl shadow-xl border border-gray-100 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-royal to-royal-dark"></div>
        <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          {isLogin ? 'Welcome Back' : 'Create an Account'}
        </h3>
        
        {error && (
          <div className="mb-4 bg-red-50 border-l-4 border-red-500 p-4 rounded text-red-700 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input type="text" name="name" onChange={handleChange} required className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-royal focus:outline-none transition-shadow" placeholder="John Doe" />
            </div>
          )}
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input type="email" name="email" onChange={handleChange} required className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-royal focus:outline-none transition-shadow" placeholder="you@example.com" />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input type="password" name="password" onChange={handleChange} required className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-royal focus:outline-none transition-shadow" placeholder="••••••••" />
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Education Level</label>
              <select name="education" onChange={handleChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-royal focus:outline-none transition-shadow">
                <option value="Grade 10">Grade 10</option>
                <option value="Grade 12 Science(PCM)">Grade 12 Science(PCM)</option>
                <option value="Grade 12 Science(PCB)">Grade 12 Science(PCB)</option>
                <option value="Grade 12 Science(PCMB)">Grade 12 Science(PCMB)</option>
                <option value="Grade 12 Commerce">Grade 12 Commerce</option>
                <option value="Grade 12 Arts">Grade 12 Arts</option>
                <option value="Diploma/Polytechnic">Diploma/Polytechnic</option>
                <option value="UG">Undergraduate (UG)</option>
              </select>
            </div>
          )}
          
          <button type="submit" className="w-full bg-royal hover:bg-royal-dark text-white font-semibold py-3 px-4 rounded-lg transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 mt-6">
            {isLogin ? 'Sign In' : 'Register'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button onClick={() => setIsLogin(!isLogin)} className="text-royal font-semibold hover:underline">
            {isLogin ? 'Register here' : 'Login here'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default Home;
