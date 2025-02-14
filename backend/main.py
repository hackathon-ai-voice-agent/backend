from fastapi import FastAPI, File, UploadFile
import os
import shutil
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI()


# 🔥 Enable CORS for frontend requests 🔥
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
UPLOAD_DIR = "uploads"
OUTPUT_FILE = "ai_response.mp3"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    """Receive an audio file, process it, and return AI-generated voice response."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    transcription = transcribe_audio(file_path)
    if not transcription:
        return {"error": "Failed to transcribe audio"}
    
    ai_response = get_ai_response(transcription)
    text_to_speech(ai_response)
    
    return FileResponse(OUTPUT_FILE, media_type="audio/mpeg", filename="response.mp3")

def transcribe_audio(file_path):
    """Transcribe audio to text using OpenAI Whisper."""
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
            return transcript.text
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None

def get_ai_response(user_input):
    """Generate a response from OpenAI GPT-4."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"GPT-4 error: {str(e)}")
        return "I'm sorry, but I couldn't process your request."

def text_to_speech(text):
    """Convert AI response to speech and save it as an audio file."""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="ash",
            input=text,
        )
        response.stream_to_file(OUTPUT_FILE)
    except Exception as e:
        print(f"TTS error: {str(e)}")
