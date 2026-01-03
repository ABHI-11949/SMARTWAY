from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from websocket import websocket_endpoint  # your endpoint using camera + MediaPipe

app = FastAPI()

# WebSocket endpoint
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket_endpoint(websocket)

# Root route
@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h2>Project Running ✅</h2><p>Open teacher/student dashboard to see live status.</p>"
