from fastapi import FastAPI

app = FastAPI()

@app.get("/saludar")
async def saludar():
    return {"Hola": "Mundo"}
@app.post("/saludar/post")
async def post():
    return {"Hola": "Post"}
@app.put("/saludar/put")
async def put():
    return {"Hola": "Put"}
@app.delete("/saludar/delete")
async def delete():
    return {"Hola": "Delete"}
