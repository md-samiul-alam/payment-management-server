from fastapi import FastAPI, HTTPException
import config.database as db
import random
from models.payee import PayeeInfo
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

@app.get("/payees", response_model=List[PayeeInfo])
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

@app.post("/payees", response_model=PayeeInfo)
async def create_payee(payee: PayeeInfo):
    try:
        payee_dict = payee.model_dump()
        
        result = db.payee_collection.insert_one(payee_dict)
        
        created_payee = db.payee_collection.find_one({"_id": result.inserted_id})
        
        created_payee["id"] = str(created_payee["_id"])
        
        return created_payee
    except Exception as e:
        if "duplicate key error" in str(e):
            raise HTTPException(
                status_code=400,
                detail="A payee with this email already exists"
            )
        raise HTTPException(status_code=500, detail=str(e))

