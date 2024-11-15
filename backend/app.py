from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import whisper
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Pa88W*r3@localhost:3306/transcription_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ensure the 'uploads' folder exists before saving the file
#if not os.path.exists('uploads'):
    #os.makedirs('uploads')

model = whisper.load_model("tiny")

class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_filename = db.Column(db.String(100), nullable=False)
    transcribed_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Check if a file was sent with the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    # Get the uploaded file from the request
    file = request.files['file']

    # Check if a file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Ensure file extension is allowed
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # In your transcribe function, check if the file is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Secure the filename and save it to the 'uploads' folder
    filename = secure_filename(file.filename)
    uploads_dir = os.path.join(os.getcwd(), 'uploads')

    # Ensure the 'uploads' folder exists before saving the file
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    file_path = os.path.join(uploads_dir, filename)
    file.save(file_path)
    print(f"File saved at: {file_path}")  # Print the path for debugging

    # Check if the file exists before attempting to transcribe
    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{filename}' not found."}), 400

    # Transcribe the audio using Whisper
    #audio_file_path ="{file_path}"
    try:
        result = model.transcribe(file_path)
        transcribed_text = result['text']
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

    # Save the transcription in the database
    transcription = Transcription(audio_filename=filename, transcribed_text=transcribed_text)
    db.session.add(transcription)
    db.session.commit()

    # Return the transcription as JSON response
    return jsonify({
        "audio_filename": filename,
        "transcribed_text": transcribed_text
    }), 201

@app.route('/transcriptions', methods=['GET'])
def get_transcriptions():
    transcriptions = Transcription.query.all()
    return jsonify([
        {"audio_filename": t.audio_filename, "transcribed_text": t.transcribed_text, "created_at": t.created_at}
        for t in transcriptions
    ]), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# Route to search transcriptions by audio filename
@app.route('/search', methods=['GET'])
def search_transcriptions():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Filename query parameter is required"}), 400

    transcriptions = Transcription.query.filter(Transcription.audio_filename.contains(filename)).all()
    return jsonify([
        {"audio_filename": t.audio_filename, "transcribed_text": t.transcribed_text, "created_at": t.created_at}
        for t in transcriptions
    ]), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
