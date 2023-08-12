from fastapi import FastAPI
from give_proxy.router import router as give_rout

app = FastAPI()

app.include_router(give_rout)