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


# --- Dummy endpoint to verify end-to-end deployment ---
DEMO_PRODUCTS = [
    {"id": 1, "name": "ECS Cluster Pro", "category": "Compute", "price": 49.99, "in_stock": True},
    {"id": 2, "name": "ALB Traffic Shield", "category": "Networking", "price": 29.99, "in_stock": True},
    {"id": 3, "name": "Fargate Task Runner", "category": "Compute", "price": 19.99, "in_stock": False},
    {"id": 4, "name": "ECR Image Vault", "category": "Storage", "price": 9.99, "in_stock": True},
    {"id": 5, "name": "CloudWatch Lens", "category": "Observability", "price": 14.99, "in_stock": True},
]

@app.get("/products")
def get_products():
    return {
        "count": len(DEMO_PRODUCTS),
        "source": "demo-data",
        "deployed_on": "ECS Fargate",
        "products": DEMO_PRODUCTS,
    }

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in DEMO_PRODUCTS if p["id"] == product_id), None)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product