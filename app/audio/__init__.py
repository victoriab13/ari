import os
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
# import openai  # Only needed for transcription and TTS

load_dotenv()

def process_audio(audio_data, agent_prompt):
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_data)
        temp_audio_path = temp_audio.name

    print(f"Saved audio to: {temp_audio_path}")
    print(f"File size: {os.path.getsize(temp_audio_path)} bytes")

    try:
        # 1. Transcribe audio using whisper-1 (REST API)
        try:
            import openai  # Only for transcription and TTS
            openai.api_key = os.getenv("OPENAI_API_KEY")
            with open(temp_audio_path, "rb") as audio_file:
                transcription = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            user_text = transcription if isinstance(transcription, str) else getattr(transcription, "text", str(transcription))
            print("Transcription:", user_text)
        except Exception as e:
            print("TRANSCRIPTION FAILED:", e)
            user_text = "Hello (transcription failed)"

        if not user_text or not isinstance(user_text, str):
            user_text = "Hello"

        # 2. Only use user input for classic audio endpoints (not for Realtime API)
        combined_input = user_text
        print("Input for TTS:", repr(combined_input))

        # 3. (Placeholder) Here you could call a model or return a canned response
        reply = "This is a placeholder response from the Realtime API."

        # 4. Use OpenAI TTS to generate audio from reply
        try:
            speech_response = openai.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=reply
            )
            response_audio = speech_response.content
            print(f"Returning TTS audio of length: {len(response_audio)} bytes")
            return response_audio
        except Exception as e:
            print("TTS FAILED:", e)
            return b""

    except Exception as e:
        print("EXCEPTION CAUGHT!")
        print(f"Transcription or TTS error: {e}")
        return b""
    finally:
        os.remove(temp_audio_path)