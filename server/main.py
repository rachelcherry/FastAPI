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
@app.get("/products/count") # sets the route
async def get_count():
    try:
        number = await app.state.db.fetch("SELECT COUNT(*) FROM products") # query to get the count from the products list
        return {"count": number} # return the number of total products
    except Exception as error: # if the number is not able to be fetched
        print(error)
        raise HTTPException(status_code=500, detail="Count was not returned properly.") # throw a status 500 error 


# get request to get all products in the database
# your code here
@app.get("/products") # sets the route
async def get_products(limit: int = 10, page: int = 1): 
    try:
        offset = ( page - 1 ) * limit # sets the offset for each page to be whatever page we are on minus one times the limit. This will ensure that we are selecting the correct products
        query = await app.state.db.fetch("SELECT * FROM products LIMIT $1 OFFSET $2", limit, offset) # query to get the products according to the limit and offset 
        return {"products": query} # return the products according to the pagination
    except Exception as error: # if any of the above steps do not work (i.e. server error)
        print(error)
        raise HTTPException(status_code=500, detail="Products with pagination were not returned correctly") # throw a states 500 error


# get request to get a product by its id
# your code here
@app.get("/products/{prod_id}")
async def get_ID(prod_id : int):
    try:
        id = await app.state.db.fetchrow("SELECT * FROM products WHERE id=$1", prod_id) # query to get the product according to the product id given
        if id is None: # if the id does not exist 
            raise HTTPException(status_code=404, detail="product was not found.") # throw a status 404 error, which shows that the product cannot be found
        else:
            return {"id": id} # if the id can be found, then return the product specified
    
    except Exception as error: # if any of the above steps do not work (i.e. server error)
        print(error)
        raise HTTPException(status_code=500, detail="Product was not returned correctly") # throw a status 500 error 



# ======================================== run the app =========================================
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

# ==============================================================================================