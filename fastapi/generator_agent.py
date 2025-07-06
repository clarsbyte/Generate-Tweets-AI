from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from twitter_interfacing import GetTweets
import os
import json
import re

load_dotenv()
os.getenv('GOOGLE_API_KEY')

prompt = """
# Role
You are a tweet generator. You write tweets based on the user's inputted topic using the writing style of an X user inputted.

# Instruction
1. Research about topic
2. Analyze writing style of reference tweets. Make sure to use the get_reference_tweets tool to get the tweets.
3. Create a tweet with writing style based on the inputted tweets. 

# Rules
1. Make sure the generated tweet matches the style of inputted tweets
2. Match everything, from grammar, uppercase or lowercase, to punctuation
3. Only analyze writing style and personality. Not reuse topics from the tweets.
4. Reusing tweets is NOT advisable. I REPEAT, IT IS NOT ADVISABLE. DO NOT COPY TWEETS>

# Output
5 Generated Tweets with identic writing style of reference tweets. Output the tweets as a JSON with this format:
{"tweets": [
    "tweet 1",
    "tweet 2",
    "tweet 3",
    "tweet 4",
    "tweet 5"
    ]}

----------

EXAMPLE:

Input: Create a tweet about how I like cats.
<tweet 1> man what's going on with the job market<tweet 1/>

<tweet 2> i need to lock in asap god <tweet2/>

<tweet 3> bro its raining hard today<tweet 3/>

Analyzing (Thinking process):
Okay, so the user doesn't use emojis and is probably gen z so let's use a little bit of gen z slang. All tweets are lowercase so let's use lowercase. They are more informal.

Output | Not yet converted to JSON (one of them): 
<correct>man cats are so goated<correct/>

<incorrect>rather than locking in, lets love cats<incorrect/>

-> Why incorrect? 
Because it copies word for word of the second tweet! We only want to analyze personality, not copy topics.
"""


generator_agent = Agent(
    'gemini-2.5-flash',
    system_prompt=prompt,
    deps_type=str
)

@generator_agent.tool
def get_reference_tweets(ctx: RunContext[str]) -> list:
    GetTweets(ctx.deps).get()
    with open('tweets.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    tweets = [tweet['text'] for tweet in data if 'text' in tweet]
    return tweets 

def parse_clean_json_response(raw_response):
    """
    Parse the clean JSON response for frontend
    """
    try:
        json_pattern = r'```json\s*\n(.*?)\n```'
        match = re.search(json_pattern, raw_response, re.DOTALL)
        
        if not match:
            raise ValueError("No JSON code block found")
        
        json_string = match.group(1).strip()
        
        data = json.loads(json_string)
        
        formatted_tweets = []
        
        for i, tweet_text in enumerate(data.get('tweets', []), 1):
            tweet_obj = {
                "text": tweet_text,  
            }
            formatted_tweets.append(tweet_obj)
        
        return {
            "tweets": formatted_tweets,
        }
        
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON: {str(e)}",
            "tweets": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}",
            "tweets": []
        }


def generate_tweets(topic, username):
    result = generator_agent.run_sync(topic, deps=username)
    return parse_clean_json_response(result.output)



