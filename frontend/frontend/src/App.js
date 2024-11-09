import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [transcriptions, setTranscriptions] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);

  // Handle file change
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle file upload
  const handleFileUpload = async () => {
    if (!file) return alert("Please select a file.");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5000/transcribe", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      // After successful upload, fetch transcriptions
      fetchTranscriptions();
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file");
    } finally {
      setLoading(false);
    }
  };

  // Fetch all transcriptions from the database
  const fetchTranscriptions = async () => {
    try {
      const response = await axios.get("http://localhost:5000/transcriptions");
      setTranscriptions(response.data);
    } catch (error) {
      console.error("Error fetching transcriptions:", error);
    }
  };

  // Search transcriptions by audio filename
  const handleSearch = async () => {
    if (!searchQuery) return fetchTranscriptions();

    try {
      const response = await axios.get("http://localhost:5000/search", {
        params: {
          filename: searchQuery,
        },
      });
      setTranscriptions(response.data);
    } catch (error) {
      console.error("Error searching transcriptions:", error);
    }
  };

  return (
    <div className="App">
      <h1>Transcription App</h1>

      {/* File upload */}
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload File"}
      </button>

      {/* Search bar */}
      <div>
        <input
          type="text"
          placeholder="Search by filename"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {/* Display transcriptions */}
      <ul>
        {transcriptions.map((transcription, index) => (
          <li key={index}>
            <strong>{transcription.audio_filename}</strong>: {transcription.transcribed_text}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
