from fastapi import FastAPI

app = FastAPI(title="FastAPI Chat App")


@app.get("/")
async def get_root():
    """
    Root endpoint to check if the server is running.
    """
    return {"message": "FastAPI Chat Server is running!"}
