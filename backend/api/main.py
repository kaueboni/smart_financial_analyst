# main.py - FastAPI entrypoint
from fastapi import FastAPI

app_fastapi = FastAPI()

# Example root endpoint
@app_fastapi.get("/")
def read_root():
	return {"message": "Backend is running!"}
