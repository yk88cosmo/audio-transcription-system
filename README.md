# audio-transcription-system
Architecture Overview

The application consists of the following components:

    Frontend:
        Built using React for the user interface.
        Allows users to upload audio files, view transcriptions, and search through transcriptions.

    Backend:
        Built using Flask to serve as the API for interacting with the frontend.
        Contains endpoints for health check (/health), file upload and transcription (/transcribe), retrieving all transcriptions (/transcriptions), and searching transcriptions (/search).
        Uses the Whisper model from Hugging Face to transcribe audio files.

    Database:
        A MySQL or SQLite database is used to store transcriptions along with the audio filename and timestamp.
        SQLAlchemy ORM is used to manage the database interactions.

    External Services:
        Whisper is used to perform speech-to-text conversion on the uploaded audio files.

You can find a visual representation of this architecture in the architecture.pdf file.