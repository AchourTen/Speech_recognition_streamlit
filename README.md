# Speech_recognition_streamlit

A Streamlit-based speech recognition application that provides real-time transcription with pause/resume functionality and multiple export options.

## Features

- Real-time speech-to-text transcription
- Support for multiple languages (English, French, Spanish)
- Pause and resume recording capability
- Multiple export formats (TXT, JSON, CSV)
- Transcript history
- Offline recognition support using CMU Sphinx
- Ambient noise adjustment
- Timestamp inclusion in saved transcripts
- Custom save directory options
- Direct file download capability

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AchourTen/Speech_recognition_streamlit.git
cd Speech_recognition_streamlit
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Requirements

Create a `requirements.txt` file with these dependencies:
```
streamlit
SpeechRecognition
pyaudio
pocketsphinx
```

Note: PyAudio installation might require additional system dependencies:
- On Ubuntu/Debian: `sudo apt-get install python3-pyaudio`
- On Windows: Install from wheel file if pip installation fails
- On macOS: `brew install portaudio`

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Navigate to the provided local URL (typically http://localhost:8501)

3. Use the interface to:
   - Select your preferred language
   - Choose between online (Google) or offline (Sphinx) recognition
   - Start/Stop recording
   - Pause/Resume during recording
   - Save transcripts in various formats

## Features in Detail

### Recording Controls
- **Start Recording**: Begins a new transcription session
- **Stop Recording**: Ends the current session and adds to history
- **Pause/Resume**: Temporarily halts recording without ending the session

### Save Options
- **File Formats**:
  - TXT: Plain text with optional timestamp
  - JSON: Structured format with timestamp and text
  - CSV: Spreadsheet format with timestamp and text columns
- **Timestamp Options**: Include/exclude timestamps in saved files
- **Custom Directory**: Specify save location
- **Download**: Direct download of saved transcripts

### Language Support
- English (en-US)
- French (fr-FR)
- Spanish (es-ES)

## Project Structure

```
speech-recognition-app/
├── app.py
├── requirements.txt
├── README.md
├── transcripts/
   └── (saved transcripts)
```

## Troubleshooting

1. **Microphone Issues**
   - Ensure your microphone is properly connected
   - Check system permissions for microphone access
   - Verify PyAudio installation

2. **Recognition Errors**
   - Check internet connection for Google recognition
   - Adjust microphone position
   - Ensure quiet environment for better accuracy

3. **Save Errors**
   - Verify write permissions in save directory
   - Ensure adequate disk space
   - Check for valid file paths

## Contributing

1. Fork the repository
2. Open a Pull Request

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Google Speech-to-Text API](https://cloud.google.com/speech-to-text)
- [CMU Sphinx](https://cmusphinx.github.io/)
