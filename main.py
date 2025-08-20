from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def get_hotels():
    return "Hello"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
