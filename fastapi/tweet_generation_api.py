from fastapi import FastAPI, Request, status
import uvicorn
from fastapi.params import Body
from generator_agent import generate_tweets
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import json
import sqlite3


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="clarissassecrethahaha")

def init_db():
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            username TEXT,
            tweets TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.post("/generate-tweets")
def get_tweets(request: Request, input: dict = Body(...)):
    result = generate_tweets(input['topic'], input['username'])
    
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO generated_tweets (topic, username, tweets) VALUES (?, ?, ?)",
        (input['topic'], input['username'], json.dumps(result))  
    )
    conn.commit()
    conn.close()
    
    return result


@app.get("/results")
def get_latest_tweets():
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT tweets FROM generated_tweets ORDER BY created_at DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    if result: 
        return json.loads(result[0])  
    return []

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)