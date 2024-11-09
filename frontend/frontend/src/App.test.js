import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import axios from 'axios';

// Mock Axios
jest.mock('axios');

describe('App', () => {
  it('should upload a file successfully', async () => {
    // Mock successful response for file upload
    axios.post.mockResolvedValue({ data: { success: true } });

    render(<App />);

    const fileInput = screen.getByLabelText(/Upload File/i);
    const file = new File(['audio content'], 'test_audio.wav', { type: 'audio/wav' });
    fireEvent.change(fileInput, { target: { files: [file] } });

    const uploadButton = screen.getByText(/Upload File/i);
    fireEvent.click(uploadButton);

    await waitFor(() => expect(axios.post).toHaveBeenCalledTimes(1));
    expect(axios.post).toHaveBeenCalledWith('http://localhost:5000/transcribe', expect.any(FormData), expect.any(Object));
  });

  it('should display transcriptions', async () => {
    // Mock response for transcriptions
    const transcriptions = [
      { audio_filename: 'test_audio.wav', transcribed_text: 'This is a test transcription.' },
    ];
    axios.get.mockResolvedValue({ data: transcriptions });

    render(<App />);

    // Wait for the list of transcriptions to appear
    await waitFor(() => screen.getByText('This is a test transcription.'));
    expect(screen.getByText('This is a test transcription.')).toBeInTheDocument();
  });

  it('should search transcriptions correctly', async () => {
    const transcriptions = [
      { audio_filename: 'test_audio.wav', transcribed_text: 'This is a test transcription.' },
      { audio_filename: 'another_audio.wav', transcribed_text: 'Another transcription.' },
    ];
    axios.get.mockResolvedValue({ data: transcriptions });

    render(<App />);

    // Wait for the transcriptions to load
    await waitFor(() => screen.getByText('This is a test transcription.'));

    const searchInput = screen.getByPlaceholderText(/Search by filename/i);
    fireEvent.change(searchInput, { target: { value: 'test_audio.wav' } });

    const searchButton = screen.getByText('Search');
    fireEvent.click(searchButton);

    await waitFor(() => screen.getByText('This is a test transcription.'));
    expect(screen.queryByText('Another transcription.')).toBeNull();
  });
});
