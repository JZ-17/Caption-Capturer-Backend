from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
import tempfile
from googletrans import Translator

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Whisper model
model = whisper.load_model("base")
translator = Translator()

@app.route("/translate", methods=["POST"])
def translate():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        language = request.form.get("language", "en")
        audio_file = request.files["audio"]

        # Save audio to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            audio_path = temp_file.name
            audio_file.save(audio_path)

        # Transcribe audio
        result = model.transcribe(audio_path)
        transcription = result["text"]

        # Translate text
        translated_text = translator.translate(transcription, dest=language).text

        # Clean up temp file
        os.remove(audio_path)

        return jsonify({"translation": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
