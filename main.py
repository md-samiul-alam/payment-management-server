from fastapi import FastAPI, HTTPException
import config.database as db
import random
from models.payee import PayeeInfo
from typing import List
from bson import ObjectId

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
    

@app.get("/payees/{payee_id}", response_model=PayeeInfo)
async def get_payee_by_id(payee_id: str):
    try:
        if not ObjectId.is_valid(payee_id):
            raise HTTPException(status_code=400, detail="Invalid payee ID format")
            
        payee = db.payee_collection.find_one({"_id": ObjectId(payee_id)})
        
        if not payee:
            raise HTTPException(status_code=404, detail="Payee not found")
            
        payee["id"] = str(payee["_id"])
        
        return payee
    except HTTPException as he:
        raise he
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

