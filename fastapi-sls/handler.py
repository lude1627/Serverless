from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from routers.router import array_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



for router in array_router:
    print(router)
    app.include_router(router)

handler = Mangum(app)
