"use client";
import React from 'react';
import { useState } from 'react';
import axios from 'axios';

const GenerateTweets = () => {
  const [username, setUsername] = useState('');
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);

  const api = axios.create({
    baseURL: 'http://localhost:8000'
  });

  const handleSubmit = async () => {
    if (!username || !topic) {
      alert('Please fill in both fields.');
      return;
    }

    setLoading(true);
    
    try {
      const response = await api.post('/generate-tweets', {
        username: username,
        topic: topic
      });
      
      console.log('API Response:', response.data);
      
    } catch (error) {
      console.error('Error generating tweets:', error);
      alert('Error generating tweets. Please try again.');
    } finally {
      setLoading(false);
      window.location.href = '/results'; 
    }
  };

  const checkUsername = (user: string) => {
    const trimmedUser = user.trim();
    
    if (trimmedUser.includes('@')) {
      alert('Username cannot contain @ symbols.');
      return;
    }
    setUsername(user);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-50 to-white relative overflow-hidden p-6">
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-50 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-100/50 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-blue-50/30 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className="relative z-10 flex flex-col items-center justify-center min-h-[80vh] px-3">
        <div className="max-w-2xl mx-auto w-full">
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-blue-900 mb-4">
              Generate Your{' '}
              <span className="bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                Perfect Tweets
              </span>
            </h1>
            <p className="text-lg text-blue-700">
              Generate five tweets in one output.<br/> Please wait as we analyze the tweets first.
            </p>
          </div>

          <div className="bg-blue-50 rounded-3xl p-8 md:p-7 border border-blue-100 shadow-lg hover:shadow-xl transition-all duration-300">
            <div className="space-y-8">
              <div className="space-y-3">
                <div className="block text-blue-800 font-semibold text-lg">
                  What account would you like to tweet like?
                </div>
                <input 
                  className="w-full px-6 py-4 border-2 border-blue-200 rounded-xl bg-white text-blue-900 placeholder-blue-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition-all duration-300 text-lg"
                  name="username" 
                  type="text"
                  placeholder="Username without @"
                  onChange={(e) => {checkUsername(e.target.value)}}
                  disabled={loading}
                />
              </div>

              <div className="space-y-3">
                <div className="block text-blue-800 font-semibold text-lg">
                  What do you want to tweet about?
                </div>
                <input 
                  className="w-full px-6 py-4 border-2 border-blue-200 rounded-xl bg-white text-blue-900 placeholder-blue-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition-all duration-300 text-lg"
                  name="topic" 
                  type="text"
                  placeholder="The fact that I love cats"
                  onChange={(e) => {setTopic(e.target.value)}}
                  disabled={loading}
                />
              </div>

              <div className="pt-4">
                <button 
                  onClick={handleSubmit}
                  disabled={loading}
                  className="w-full group relative px-8 py-5 bg-blue-600 text-white font-semibold text-lg rounded-xl hover:bg-blue-700 transition-all duration-300 transform hover:scale-[1.02] hover:shadow-xl shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span className="relative z-10 flex items-center justify-center space-x-2">
                    {loading ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        <span>Generating...</span>
                      </>
                    ) : (
                      <span>Generate Tweets</span>
                    )}
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-800 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </button>
              </div>
            </div>
          </div>          
        </div>
      </div>
    </div>
  );
};

export default GenerateTweets;