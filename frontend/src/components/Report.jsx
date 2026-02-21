import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import html2pdf from 'html2pdf.js';
import api from '../api';

const Report = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const reportRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await api.get('/career_roadmap');
        if (res.data.success) {
          setReportData(res.data.roadmap);
        } else {
          // If no roadmap exists yet, go to dashboard
          navigate('/main');
        }
      } catch (err) {
        console.error("Error fetching roadmap:", err);
        navigate('/main');
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [navigate]);

  const downloadPDF = () => {
    const element = reportRef.current;
    if (!element) return;
    
    const opt = {
      margin: 0.5,
      filename: 'Career_Guider_Roadmap.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    
    html2pdf().set(opt).from(element).save();
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-[60vh] gap-4">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-royal"></div>
        <p className="text-royal font-semibold text-lg animate-pulse">Llama is analyzing your profile...</p>
      </div>
    );
  }

  // Very basic Markdown parser to format the Llama response
  // Assuming headings use `##` and lists use `*` or `-`
  const formattedReport = reportData
    ?.split('\\n')
    .map((line, idx) => {
      if (line.startsWith('###')) return <h3 key={idx} className="text-xl font-bold mt-6 mb-2 text-[#1f2937]">{line.replace('###', '')}</h3>;
      if (line.startsWith('##')) return <h2 key={idx} className="text-2xl font-bold mt-8 mb-4 border-b pb-2 text-[#2563eb]">{line.replace('##', '')}</h2>;
      if (line.startsWith('#')) return <h1 key={idx} className="text-3xl font-extrabold mt-8 mb-4 text-[#1d4ed8]">{line.replace('#', '')}</h1>;
      if (line.startsWith('- ') || line.startsWith('* ')) return <li key={idx} className="ml-6 mb-1 text-[#374151]">{line.substring(2)}</li>;
      if (line.trim() === '') return <br key={idx} />;
      return <p key={idx} className="mb-2 text-[#374151] leading-relaxed">{line}</p>;
    });

  return (
    <div className="max-w-4xl mx-auto mt-8 mb-16">
      <div className="flex justify-between items-center mb-6 px-4">
        <button 
          onClick={() => navigate('/main')}
          className="text-gray-500 hover:text-royal font-medium transition flex items-center gap-2"
        >
          ← Back to Dashboard
        </button>
        <button 
          onClick={downloadPDF}
          className="bg-royal hover:bg-royal-dark text-white font-semibold py-2 px-6 rounded-lg shadow transition flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          Download PDF
        </button>
      </div>

      <div 
        ref={reportRef} 
        className="bg-[#ffffff] rounded-2xl shadow-2xl p-10 md:p-14 border border-[#f3f4f6]"
      >
        <div className="text-center mb-8 border-b border-[#f3f4f6] pb-8">
          <h1 className="text-4xl font-extrabold text-[#111827] tracking-tight">Your Career Roadmap</h1>
          <p className="text-[#6b7280] mt-3 text-lg">AI-Generated personalized recommendations based on your distinct profile.</p>
        </div>
        
        <div className="max-w-none">
          {formattedReport}
        </div>
      </div>
    </div>
  );
};

export default Report;
