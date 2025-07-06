"use client";
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';

const Results = () => {
  const [copiedId, setCopiedId] = useState(null);
  const [generatedTweets, setGeneratedTweets] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

    const api = axios.create({
    baseURL: 'http://localhost:8000'
  });

  useEffect(() => {
    const fetchTweets = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await api.get('/results');
        if (response.status === 200) {
          setGeneratedTweets(response.data.tweets || []);
        } else {
          throw new Error('Failed to fetch tweets');
        }
      } catch (error) {
        console.error('Error fetching tweets:', error);
        setError(error.message);
        setGeneratedTweets([]);
      } finally {
        setIsLoading(false);
      }
    }
    
    fetchTweets();
  }, []);

  const copyToClipboard = async (text: string, id: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-blue-600 text-xl">Loading tweets...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-red-600 text-xl">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white relative overflow-hidden">
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-50 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-100/50 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-blue-50/30 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className="relative z-10 px-6 pb-12">
        <div className="max-w-4xl mt-10 mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-blue-900 mb-4">
              Your{' '}
              <span className="bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                Generated Tweets
              </span>
            </h1>
            <p className="text-lg text-blue-700 mb-6">
              Generated tweets ready to use!
            </p>
          </div>

          {generatedTweets.length === 0 ? (
            <div className="text-center text-blue-600">
              <p>No tweets found. Generate some tweets first!</p>
              <Link href='/'>
                <button className="mt-4 px-8 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-all duration-300">
                  Generate Tweets
                </button>
              </Link>
            </div>
          ) : (
            <div className="space-y-6">
              {generatedTweets.map((tweet, index) => (
                <div 
                  key={index}
                  className="bg-blue-50 rounded-2xl p-6 border border-blue-100 hover:bg-blue-100 transition-all duration-300 group relative"
                >
                  <div className="text-blue-900 text-lg leading-relaxed pr-12">
                    {tweet.text || tweet}
                  </div>
                  
                  <button 
                    onClick={() => copyToClipboard(tweet.text || tweet, index)}
                    className="absolute top-4 right-4 p-2 bg-white rounded-lg text-blue-600 hover:bg-blue-200 hover:text-blue-800 transition-all duration-300 opacity-0 group-hover:opacity-100"
                  >
                    {copiedId === index ? (
                      <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path>
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z"></path>
                        <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2H6z"></path>
                      </svg>
                    )}
                  </button>
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <div className="bg-blue-50 rounded-2xl p-6 border border-blue-100 inline-block">
              <p className="text-blue-700 mb-4">
                Love these tweets? Generate more!
              </p>
              <Link href='/'>
                <button className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-all duration-300 transform hover:scale-105">
                  Generate More Tweets
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;