from fastapi import FastAPI
import config.database as db
import random

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
