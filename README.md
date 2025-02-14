# Voice Agent Demo  

This is a simple voice-based chatbot using FastAPI and OpenAI APIs. The user speaks into the frontend, and the backend transcribes the audio, generates a response, converts it to speech, and returns the voice response.  

## Features  
✅ Record voice input from the frontend  
✅ Transcribe speech using OpenAI Whisper  
✅ Generate a response using OpenAI GPT-4  
✅ Convert the response to speech using OpenAI TTS  
✅ Play the AI response on the frontend  

## Requirements  
- Python 3.11.8  
- Install dependencies from `requirements.txt`  

## Setup  

### 1️⃣ Install Dependencies  
```bash
pip install -r requirements.txt

### 2️⃣ Set Up Environment Variables
Create a `.env` file and add:  
```env
OPENAI_API_KEY=your_openai_api_key

### 3️⃣ Run the Backend
```bash
uvicorn main:app --reload

### 4️⃣  Run the Frontend
Open index.html in your browser.


### Flow
User speaks 🎤
→ Frontend records voice
→ Sends audio to backend
→ Backend transcribes speech (Whisper)
→ Sends text to GPT-4 for response
→ Converts response to speech (TTS)
→ Sends MP3 file back to frontend
→ Frontend plays AI voice response 🔊



### API Endpoints
🎤 Upload and Get Response
```http
POST /upload/

- Input: Audio file (.wav)
- Output: AI voice response (.mp3)