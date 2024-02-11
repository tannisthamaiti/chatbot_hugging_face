# Import key libraries and packages
from fastapi import FastAPI
import pickle
import uvicorn
import os
import sys
import redis
import json
from fastapi_redis_rate_limiter import RedisRateLimiterMiddleware, RedisClient

app = FastAPI()
rd = redis.Redis(host="localhost", port=6379, db=0)
app.add_middleware(RedisRateLimiterMiddleware, redis_client=rd, limit=4, window=60)

# Define directory paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.gptj import GPT
from agents.schemas import ChatAgentResponse



# Function to load huggingface api
gpt_new= GPT()


@app.post('/predict_agent')
async def predict(query: str, car: ChatAgentResponse):
      cache=rd.get(query)
      
      if cache:
        print("hit cache")
        return cache.decode("utf-8")
      else:
        print("cache miss")
        result=gpt_new.query(query)
        rd.set(query,result[0]["generated_text"])
        rd.expire(query,5)
        return result[0]["generated_text"]

# Endpoints
if __name__=='__main__':
    uvicorn.run('main:app', reload=True)