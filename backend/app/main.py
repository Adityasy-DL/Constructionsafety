from fastapi import FastAPI

app = FastAPI(title="Construction Safety")


@app.get("/")
def root():
    return {"message": "API is running"}