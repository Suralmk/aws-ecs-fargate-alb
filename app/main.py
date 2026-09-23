from fastapi import FastAPI
import os 
import socket
import time


app = FastAPI(
    title = "AWS Contianer Lab API",
    description="A minimal API for learning AWS container deployment",
    version="1.0.0",
)

START_TIME = time.time()

@app.get("/")
def root():
    return {
        "service": "aws-container-lab",
        "message": "API is running",
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/info")
def info():
    return {
        "service": "aws-container-lab",
        "version": "1.0.0",
        "hostname": socket.gethostname(),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }

@app.get("/metrics")
def metrics():
    return {
        "uptime_sec": round(time.time() - START_TIME, 2)
    }