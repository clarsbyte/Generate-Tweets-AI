# AI Tweet Generator
Let a fun and intelligent AI agent generate tweets like anyone—purely for fun! 


https://github.com/user-attachments/assets/765db97d-29ce-45c3-b2de-bd0d326000e5
## ✨ Features

- **Style Analysis**: Analyzes grammar, punctuation, capitalization, and personality from reference tweets
- **Topic Flexibility**: Generate tweets about any topic while preserving writing style and copy the ones you like right away
- **AI-Powered**: Uses Google's Gemini AI for intelligent tweet generation
- **Modern UI**: Clean, responsive interface built with Next.js
- **RESTful API**: FastAPI backend with automatic documentation

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js, React, Tailwind CSS |
| **Backend** | FastAPI, Python |
| **AI Model** | Google Gemini 2.5 Flash |
| **Agent** | Pydantic |
| **Containerization** | Docker |

## 📋 Prerequisites

Before running this project, make sure you have:

- **Docker Desktop** installed and running
- **Node.js** (v18 or higher)
- **npm** or **yarn** package manager
- **Google AI API Key** ([Get one here](https://ai.google.dev/))

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-tweet-generator.git
cd ai-tweet-generator
```

### 2. Environment Setup
Create a `.env` file in the `fastapi` directory:
```bash
cd fastapi
echo "GOOGLE_API_KEY=your_google_ai_api_key_here" > .env
```

### 3. Backend Setup (FastAPI)
```bash
# Navigate to backend directory
cd fastapi

# Build Docker image
docker build -t tweetgenapi .

# Run the container
docker run -d -p 8000:8000 --name tweet-backend tweetgenapi
```

### 4. Frontend Setup (Next.js)
```bash
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```


## 📖 Usage

1. **Enter a Topic**: Type the subject you want to tweet about
2. **Specify Username**: Enter the Twitter/X username whose style you want to mimic
3. **Generate Tweets**: Click generate to get 5 AI-created tweets in that user's style
4. **Copy & Use**: Select your favorite generated tweet

### Example
```
Topic: "I love coffee"
Username: "elonmusk"
Output: "Coffee is literally rocket fuel for humans 🚀"
```


**⭐ If you found this project helpful, please give it a star!**
