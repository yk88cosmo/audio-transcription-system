import os
import pytest
import tempfile
from app import app, db, Transcription  # Import your Flask app and models

@pytest.fixture
def client():
    """A test client for the Flask application."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost:3306/transcription_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables before tests run
        yield client
        with app.app_context():
            db.drop_all()  # Drop tables after tests finish

def test_health(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert b'OK' in response.data

def test_post_transcribe(client):
    """Test the /transcribe POST endpoint."""
    # Create a temporary file for testing
    data = {
        'file': (open('test_audio.wav', 'rb'), 'test_audio.wav')
    }
    response = client.post('/transcribe', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    # Check that the transcription is saved to the database
    transcription = Transcription.query.first()
    assert transcription is not None
    assert transcription.audio_filename == 'test_audio.wav'

def test_get_transcriptions(client):
    """Test the /transcriptions GET endpoint."""
    # Add a sample transcription to the database
    new_transcription = Transcription(audio_filename='test_audio.wav', transcribed_text='This is a test.')
    db.session.add(new_transcription)
    db.session.commit()

    response = client.get('/transcriptions')
    assert response.status_code == 200
    assert b'This is a test.' in response.data
