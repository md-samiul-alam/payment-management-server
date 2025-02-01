from fastapi import FastAPI, HTTPException
import config.database as db


app = FastAPI()


@app.get("/")
async def read_root():
  	return {"message": "Hello, World!"}
