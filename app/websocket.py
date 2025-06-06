from fastapi import WebSocket, WebSocketDisconnect
from typing import List

active_connections: List[WebSocket] = []

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process the audio data here (e.g., transcribe, generate response)
            response = f"Received: {data}"  # Placeholder for actual processing
            await websocket.send_text(response)
    except WebSocketDisconnect:
        active_connections.remove(websocket)