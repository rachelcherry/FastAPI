# =========================================== imports =============================================

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import asyncpg


# ======================================== database setup =========================================

# Database connection details
DATABASE_URL = "postgresql://p_user:p_password@localhost:5432/product_db"

# Establishing a connection to the database
async def connect(): return await asyncpg.connect(DATABASE_URL)

# Context manager to handle the database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await connect()
    try: yield
    finally: await app.state.db.close()

# =========================================== app setup ===========================================

# Creating a FastAPI instance
app = FastAPI(lifespan=lifespan)

# Setting up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================ routing  ===========================================

# root route, testing that the connection to the database works
@app.get("/")
async def root():
    try:
        await app.state.db.execute("SELECT 1")
        return {"message": "Hello World! Database connection is successful."}
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Bye World! Database connection failed.")
    
# get request to get the count of products in the database
# your code here
@app.get("/products/count")
async def get_count():
    try:
        number = await app.state.db.fetchval("SELECT COUNT(*) FROM products")
        return {"prod_count": number}
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Count was not returned properly.")


# get request to get all products in the database
# your code here
@app.get("/products")
async def get_products(limit: int, page: int):
    try:
        offset = ( page - 1 ) * limit
        query = await app.state.db.fetch("SELECT * FROM products LIMIT $1 OFFSET $2", limit, offset)
        return {"products": query}
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error getting pagination.")


# get request to get a product by its id
# your code here
@app.get("/products/{prod_id}")
async def get_ID(prod_id : int):
    try:
        id = await app.state.db.fetchrow("SELECT * FROM products WHERE id=$1", prod_id)
        if id is None:
            raise HTTPException(status_code=404, detail="product was not found.")
        else:
            return {"product_id": id}
    
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Error getting product.")



# ======================================== run the app =========================================
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

# ==============================================================================================