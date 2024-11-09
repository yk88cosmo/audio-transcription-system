CREATE DATABASE transcription_app;
CREATE TABLE transcription (
	id INT AUTO_INCREMENT PRIMARY KEY,
    audio_filename VARCHAR(255),
    transcribed_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT * FROM transcription;