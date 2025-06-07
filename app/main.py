import os
from dotenv import load_dotenv
import httpx
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from app.audio import process_audio
from app.audio.system_message import SYSTEM_MESSAGE
from app.audio.interruptions import InterruptionManager
from app.audio.voice_config import load_voice_config, get_random_phrase

# Force load .env from the correct location (voice-webapp/.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

app = FastAPI()

# Use an absolute path for the static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

interruption_manager = InterruptionManager()
voice_config = load_voice_config()

@app.get("/")
async def get():
    index_path = os.path.join(static_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/session")
async def get_session():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        return {"error": "OPENAI_API_KEY not set in environment or .env file."}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.openai.com/v1/realtime/sessions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-realtime-preview-2024-12-17",
                "voice": "shimmer",  # <-- switched back from "sage" to "shimmer"
                "instructions": SYSTEM_MESSAGE,  # <-- Add your full prompt here
                "speed": 0.9  # Try lowering the speed for a gentler delivery
            }
        )
        print("OpenAI session response:", resp.text)
        return resp.json()

@app.get("/system_message")
async def get_system_message():
    return {"system_message": SYSTEM_MESSAGE}

@app.get("/agent_prompt")
async def agent_prompt():
    return {"system_message": SYSTEM_MESSAGE}

@app.post("/api/audio")
async def api_audio(audio: UploadFile = File(...)):
    audio_data = await audio.read()
    response_audio = process_audio(audio_data, SYSTEM_MESSAGE)
    return Response(content=response_audio, media_type="audio/wav")

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Optionally send the system message to the client as a first message
        await websocket.send_text(SYSTEM_MESSAGE)
        while True:
            audio_data = await websocket.receive_bytes()
            response_audio = process_audio(audio_data, SYSTEM_MESSAGE)
            await websocket.send_bytes(response_audio)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()