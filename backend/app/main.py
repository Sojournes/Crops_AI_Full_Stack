from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat
# from .routers import visuals # Future implementation

app = FastAPI(title="Crops AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Crops AI API is running."}
