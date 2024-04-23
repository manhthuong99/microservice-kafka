from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .di import init_di
from .adapters.apis.promotion_router import router as promotion_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(debug=True)


origins = [
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await init_di()


app.include_router(promotion_router, prefix='/promotion')

