from imp import reload
from dbconf import connClose
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from routes.api import router as api_router
#from typing import Optional




app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("connection started")
    

@app.on_event("shutdown")
async def startup_event():
    connClose()
    print("connection closed")
    
    
origins = ["http://localhost:8005"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# if __name__ == '__main__':
#     uvicorn.run("main:app", host='127.0.0.1', port=8005, log_level="info", reload=True)
#     print("running")