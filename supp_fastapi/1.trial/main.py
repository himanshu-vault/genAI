from fastapi import FastAPI, Request
import json
from pydantic import BaseModel

app = FastAPI()

items = {}

class Item(BaseModel):
    name: str

@app.get("/items")
def list_items():
    return list(items.values())

@app.post("/items")
def create_item(request: Request, item: Item):
    print('REQUEST ----- Headers:', dict(request.headers))
    print('REQUEST ----- Query Params:', dict(request.query_params))
    # print('REQUEST ----- body:', dict(request.body))
    # print('Body:', item.model_dump_json())
    item_id = len(items) + 1
    items[item_id] = {"id": item_id, "name": item.name}
    return items[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    items.pop(item_id, None)
    return {"deleted": item_id}