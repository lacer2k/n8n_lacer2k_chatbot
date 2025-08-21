# n8n Walkie-Talkie Integration Examples

## 📋 Basic Audio Response Workflow

### Node 1: Webhook Trigger
```json
{
  "httpMethod": "POST",
  "path": "webhook-test/b533d79f-b898-40da-ac8d-61039df6dce0",
  "responseMode": "responseNode"
}
```

### Node 2: Extract Audio & Metadata
```javascript
// Code Node - Extract incoming data
const audioFile = $binary.data;
const metadata = JSON.parse($json.metadata);

return [{
  json: {
    sessionId: metadata.sessionId,
    filename: metadata.filename,
    timestamp: metadata.timestamp,
    mode: metadata.mode,
    audioReceived: true
  },
  binary: {
    audio: audioFile
  }
}];
```

### Node 3: OpenAI Whisper (Transcription)
```json
{
  "resource": "audio",
  "operation": "transcribe",
  "model": "whisper-1",
  "binaryPropertyName": "audio",
  "format": "json"
}
```

### Node 4: Process & Generate Response
```javascript
// Code Node - Generate text response
const transcription = $json.text;
const sessionId = $('Extract Audio & Metadata').item.json.sessionId;

// Your logic here - AI response, database lookup, etc.
const responseText = `I heard you say: "${transcription}". Here's my response...`;

return [{
  json: {
    sessionId: sessionId,
    transcription: transcription,
    responseText: responseText,
    needsAudio: true
  }
}];
```

### Node 5: Text-to-Speech (OpenAI or ElevenLabs)
```json
{
  "resource": "audio",
  "operation": "generate",
  "model": "tts-1",
  "voice": "alloy",
  "input": "={{$json.responseText}}",
  "format": "mp3"
}
```

### Node 6: Respond to Webhook
```javascript
// Code Node - Format response
const audioBuffer = $binary.data.data;
const base64Audio = audioBuffer.toString('base64');
const sessionId = $('Process & Generate Response').item.json.sessionId;
const transcription = $('Process & Generate Response').item.json.transcription;

return [{
  json: {
    success: true,
    transcription: {
      text: transcription
    },
    audioResponse: {
      audioData: base64Audio,
      mimeType: "audio/mp3",
      duration: 5.0 // estimate or calculate
    },
    metadata: {
      sessionId: sessionId,
      timestamp: new Date().toISOString(),
      responseGenerated: true
    }
  }
}];
```

## 🔄 Advanced: Polling Response Workflow

### Webhook Response (Immediate)
```javascript
// Code Node - Immediate response
const metadata = JSON.parse($json.metadata);

// Store session for later processing
$executionData.setNodeParameter('sessionId', metadata.sessionId);
$executionData.setNodeParameter('audioFile', $binary.data);

return [{
  json: {
    success: true,
    transcription: {
      text: "Processing your message..."
    },
    status: "processing",
    sessionId: metadata.sessionId,
    estimatedWaitTime: 10000
  }
}];
```

### Background Processing Chain
1. **Transcribe Audio** (OpenAI Whisper)
2. **Generate Response** (GPT/Claude)
3. **Convert to Speech** (TTS)
4. **Store Result** (Database/Memory)

### Feedback Endpoint Workflow
```javascript
// Code Node - Check for ready response
const requestData = $json;
const sessionId = requestData.sessionId;

// Check if response is ready (from database/memory)
const response = await checkSessionResponse(sessionId);

if (response.ready) {
  return [{
    json: {
      hasResponse: true,
      audioData: response.audioBase64,
      mimeType: response.mimeType,
      transcription: response.originalText,
      sessionId: sessionId,
      timestamp: new Date().toISOString()
    }
  }];
} else {
  return [{
    json: {
      hasResponse: false,
      status: "processing",
      sessionId: sessionId
    }
  }];
}
```

## 🎯 Session Management

### Store Session Data
```javascript
// Code Node - Store session
const sessionData = {
  sessionId: $json.sessionId,
  status: 'processing',
  originalAudio: $binary.audio,
  timestamp: new Date().toISOString(),
  completed: false
};

// Store in database or memory
await storeSession(sessionData);
```

### Retrieve Session Data
```javascript
// Code Node - Retrieve session
const sessionId = $json.sessionId;
const sessionData = await getSession(sessionId);

return [{ json: sessionData }];
```

## 🔊 Audio Processing Tips

### Convert Audio Formats
```javascript
// Code Node - Convert audio format
const inputAudio = $binary.audio;
const ffmpeg = require('fluent-ffmpeg');

// Convert to MP3 if needed
const outputBuffer = await convertToMp3(inputAudio);

return [{
  binary: {
    convertedAudio: {
      data: outputBuffer,
      mimeType: 'audio/mp3'
    }
  }
}];
```

### Calculate Audio Duration
```javascript
// Code Node - Get audio duration
const audioBuffer = $binary.audio.data;
const getAudioDurationInSeconds = require('get-audio-duration');

const duration = await getAudioDurationInSeconds(audioBuffer);

return [{
  json: {
    duration: duration,
    durationFormatted: `${Math.floor(duration / 60)}:${(duration % 60).toFixed(0).padStart(2, '0')}`
  }
}];
```

## 🚀 Testing Your Workflow

### Test Webhook Response
```bash
curl -X POST "https://lacer2k.app.n8n.cloud/webhook-test/your-webhook-id" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-session-123",
    "test": true
  }'
```

### Expected Response
```json
{
  "success": true,
  "audioResponse": {
    "audioData": "base64-encoded-audio-data",
    "mimeType": "audio/mp3"
  }
}
```

## ⚠️ Important Notes

1. **Base64 Encoding**: Always encode binary audio as base64
2. **MIME Types**: Use standard MIME types (`audio/mp3`, `audio/wav`, etc.)
3. **File Size**: Keep audio responses under 5MB
4. **Duration**: Limit responses to 60 seconds max
5. **Session IDs**: Always include session ID for conversation tracking
6. **Error Handling**: Return proper error responses when processing fails

## 🔧 Configuration Variables

Set these in your n8n environment:
- `OPENAI_API_KEY` - For Whisper transcription and TTS
- `ELEVENLABS_API_KEY` - Alternative TTS service
- `DATABASE_URL` - For session storage (if using database)
- `AUDIO_STORAGE_PATH` - For temporary audio file storage