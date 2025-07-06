import React from 'react';
import Link from 'next/link'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white relative overflow-hidden">

      <div className="relative z-10 flex flex-col items-center justify-center min-h-[80vh] px-6 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold text-blue-900 mb-8 leading-tight">
            Tweet like{' '}
            <span className="bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent animate-pulse">
              anyone
            </span>
            <span className="text-blue-700">.</span>
          </h1>

          <p className="text-xl md:text-2xl text-blue-700 mb-12 max-w-2xl mx-auto leading-relaxed">
            Generate authentic tweets in any account's style with just a few clicks. 
          </p>

          <div className="space-y-6">
            <Link href='/generate-tweets'>
              <button className="group relative px-12 py-5 bg-blue-600 text-white font-semibold text-lg rounded-full hover:bg-blue-700 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl shadow-lg">
                <span className="relative z-10">Start Tweeting</span>
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-800 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>
            </Link>
            
            <p className="text-blue-500 mt-4 text-sm">
              No account required
            </p>
          </div>

  
        </div>
      </div>

      <div className="absolute bottom-0 left-0 w-full">
        <svg viewBox="0 0 1440 120" className="w-full h-auto">
          <path
            fill="rgb(239, 246, 255)"
            d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,58.7C960,64,1056,64,1152,58.7C1248,53,1344,43,1392,37.3L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"
          />
        </svg>
      </div>
    </div>
  );
}