from fastapi import FastAPI, HTTPException
import config.database as db
import random
from typing import List

app = FastAPI()


@app.get("/")

def read_root():
  return {"message": "Hello, World!"}


@app.get("/random")
def get_random_number():
  return {
    "message": "Hello, World!",
    "random_number": random.randint(1, 100),
  }

@app.get("/random/{limit}")
def get_random_number(limit: int):
  return {
    "message": "Hello, World!",
    "random_number": random.randint(1, limit),
  }

@app.get("/payees")
async def get_payees():
    try:
        payees = list(db.payee_collection.find())
        
        if not payees:
            return []
            
        for payee in payees:
            payee["id"] = str(payee["_id"])
            
        return payees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
