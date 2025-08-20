# Audio Transcription Script

This project provides multiple ways to transcribe audio files using your n8n webhook with OpenAI:

1. **Voice Recorder Web Page** - Record voice messages directly in your browser
2. **Python Script** - Download audio from URLs and send to webhook
3. **Shell Wrapper** - Easy command-line interface

## Features

- **Voice Recorder Web Page**: Modern, responsive web interface for recording voice messages
- **URL Audio Downloader**: Downloads audio files from any accessible URL
- **Automatic file type detection** and extension handling
- **Streams large files** efficiently
- **Sends to your n8n webhook** for OpenAI transcription
- **Comprehensive error handling**
- **Optional file cleanup** after processing

## Quick Start

### Option 1: Voice Recorder Web Page (Recommended)

1. Open `voice_recorder.html` in your web browser
2. Allow microphone access when prompted
3. Click the microphone button to start recording
4. Click again to stop recording
5. Add description and tags (optional)
6. Click "Send to Webhook" to transcribe

**Features:**
- 🎤 Real-time voice recording
- ⏱️ Recording timer
- 🎵 Audio playback before sending
- 📝 Metadata input (description, tags)
- 📱 Mobile-responsive design
- ✨ Beautiful, modern UI

### Option 2: Python Script

1. Install dependencies: `pip3 install -r requirements.txt`
2. Run: `python3 audio_transcription.py "https://example.com/audio.mp3"`

### Option 3: Shell Wrapper

1. Make executable: `chmod +x transcribe.sh`
2. Run: `./transcribe.sh "https://example.com/audio.mp3"`

## Requirements

- Python 3.6 or higher
- `requests` library
- Modern web browser with microphone support (for voice recorder)
- Internet connection for webhook communication

## Installation

1. Clone or download this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make scripts executable (optional):
   ```bash
   chmod +x audio_transcription.py transcribe.sh
   ```
4. **Configure the project** (optional):
   - Edit `config.js` for web interface settings
   - Edit `config.py` for Python script settings

## Configuration

### Web Interface Configuration (`config.js`)

Edit `config.js` to customize:
- **Webhook URL**: Change the n8n webhook endpoint
- **Audio Quality**: Adjust sample rates, bitrates, and channels
- **UI Settings**: Modify recording limits and display options
- **Metadata**: Configure default tags and descriptions

```javascript
const CONFIG = {
    webhook: {
        url: 'https://your-webhook-url.com',
        timeout: 30000,
        retryAttempts: 3
    },
    audio: {
        defaultSampleRate: 48000,
        defaultBitrate: 192000,
        defaultChannels: 2
    }
    // ... more options
};
```

### Python Script Configuration (`config.py`)

Edit `config.py` to customize:
- **Webhook Settings**: URL, timeout, retry attempts
- **Audio Processing**: Supported formats and quality presets
- **File Handling**: Size limits and cleanup options
- **Logging**: Log levels and file paths

```python
WEBHOOK_CONFIG = {
    'url': 'https://your-webhook-url.com',
    'timeout': 30,
    'retry_attempts': 3,
    'max_file_size': 50 * 1024 * 1024  # 50MB
}
```

## Usage

### Voice Recorder Web Page

Simply open `voice_recorder.html` in your browser. The page will:
- Request microphone permission
- Allow you to record voice messages
- Send recordings directly to your n8n webhook
- Display transcription results
- Show file storage information

### Python Script Usage

#### Basic Usage
```bash
python3 audio_transcription.py "https://example.com/audio.mp3"
```

#### Advanced Usage
```bash
# Specify output filename
python3 audio_transcription.py "https://example.com/audio.mp3" --output my_audio.mp3

# Use a different webhook URL
python3 audio_transcription.py "https://example.com/audio.mp3" --webhook "https://your-webhook.com"

# Keep the downloaded file after sending to webhook
python3 audio_transcription.py "https://example.com/audio.mp3" --keep-file

# Combine options
python3 audio_transcription.py "https://example.com/audio.mp3" --output my_audio.mp3 --keep-file
```

### Command Line Options

- `url`: The URL of the audio file to download (required)
- `--output, -o`: Specify output filename (optional)
- `--webhook, -w`: Custom webhook URL (defaults to your n8n webhook)
- `--keep-file, -k`: Keep the downloaded file after processing
- `--help, -h`: Show help message

## Examples

### Record and transcribe a voice message
1. Open `voice_recorder.html` in your browser
2. Record your message
3. Send to webhook
4. Get instant transcription

### Download and transcribe an MP3 file
```bash
python3 audio_transcription.py "https://example.com/podcast.mp3"
```

### Download with custom filename and keep the file
```bash
python3 audio_transcription.py "https://example.com/recording.wav" --output interview.wav --keep-file
```

### Use a different webhook
```bash
python3 audio_transcription.py "https://example.com/audio.m4a" --webhook "https://your-custom-webhook.com"
```

## Supported Audio Formats

The scripts support various audio formats including:
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- WebM (.webm) - from voice recorder
- And other audio formats

## Webhook Integration

All methods send audio to your n8n webhook. The webhook URL is configured in:

- **Web Interface**: `config.js` → `CONFIG.webhook.url`
- **Python Script**: `config.py` → `WEBHOOK_CONFIG['url']`

**Default webhook URL:**
`https://lacer2k.app.n8n.cloud/webhook-test/b533d79f-b898-40da-ac8d-61039df6dce0`

**To change the webhook URL:**
1. Edit `config.js` for the web interface
2. Edit `config.py` for the Python script
3. Restart the application/script

### ⚠️ Important: Field Naming Requirement

**The field name in the multipart form data MUST match the filename** to ensure proper n8n binary property structure.

**Expected webhook output format:**
```json
{
  "binary": {
    "recording.webm": {
      "data": "<base64-data>",
      "mimeType": "audio/webm",
      "fileName": "recording.webm"
    }
  }
}
```

### Voice Recorder (Multipart Form Data)
- **Field name**: Uses the actual filename (e.g., `recording-2024-01-15T10-30-00-000Z.webm`)
- **Audio file**: Sent in the field named after the filename
- **Metadata**: Includes description, tags, timestamp, and source information
- **Format**: WebM audio for optimal web compatibility

### Python Script (Multipart Form Data)
- **Field name**: Uses the actual filename from the downloaded file
- **Audio file**: Sent in the field named after the filename
- **Handles**: Various audio formats automatically
- **Streams**: Large files efficiently

### Testing Your Webhook

Use the included `test_webhook.html` file to verify your webhook is working correctly:

1. Open `test_webhook.html` in your browser
2. Select an audio file
3. Upload to your webhook
4. Verify the response contains the expected binary property structure

This test page will show you exactly what your webhook receives and help debug any issues.

## Response Handling

### Success Response
The webhook returns detailed information including:
- Transcription text
- File details (name, size, type)
- Google Drive storage information
- Processing timestamp

### Error Handling
Comprehensive error handling for:
- Network connection issues
- Invalid URLs
- File download failures
- Webhook communication errors
- File system operations
- Microphone access issues

## Troubleshooting

### Voice Recorder Issues
1. **Microphone access denied**: Check browser permissions and allow microphone access
2. **Recording not working**: Ensure you're using HTTPS or localhost (required for getUserMedia)
3. **Audio not playing**: Check if your browser supports WebM audio format

### Common Issues
1. **Permission denied**: Make sure you have write permissions in the current directory
2. **Network errors**: Check your internet connection and the URL accessibility
3. **Webhook errors**: Verify the webhook URL is correct and accessible
4. **File format issues**: Ensure the URL points to a valid audio file

### Browser Compatibility
The voice recorder works best with:
- Chrome/Chromium (recommended)
- Firefox
- Safari (may have limited WebM support)
- Edge

## Advanced Features

### Voice Recorder
- Real-time recording with visual feedback
- Recording timer and status updates
- Audio playback before sending
- Metadata input for better organization
- Responsive design for mobile devices

### Python Script
- Automatic file type detection
- Efficient streaming for large files
- Configurable webhook endpoints
- Optional file retention

## Security Considerations

- The voice recorder runs entirely in your browser
- Audio is sent directly to your n8n webhook
- No audio data is stored locally (unless using --keep-file)
- Consider adding authentication to your webhook for production use

## License

This project is provided as-is for educational and personal use.
