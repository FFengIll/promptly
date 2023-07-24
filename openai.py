import uvicorn
import json
from fastapi import openapi
from prompt.server.server import app

if __name__ == "__main__":
    with open("openai.json", "w") as fd:
        schema = app.openapi()
        json.dump(schema, fd,indent=4,ensure_ascii=False)
