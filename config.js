// Configuration file for Audio Transcription Project
// Modify these settings as needed

const CONFIG = {
    // Webhook Configuration
    webhook: {
        url: 'https://lacer2k.app.n8n.cloud/webhook-test/b533d79f-b898-40da-ac8d-61039df6dce0',
        timeout: 30000, // 30 seconds timeout
        retryAttempts: 3,
        // Walkie-talkie specific endpoints
        feedbackUrl: 'https://lacer2k.app.n8n.cloud/webhook-test/walkie-talkie-feedback',
        statusUrl: 'https://lacer2k.app.n8n.cloud/webhook-test/walkie-talkie-status'
    },
    
    // Audio Recording Configuration
    audio: {
        defaultSampleRate: 48000,
        defaultBitrate: 192000,
        defaultChannels: 2,
        supportedFormats: [
            'audio/webm;codecs=opus;rate=48000',
            'audio/webm;codecs=opus;rate=44100',
            'audio/webm;codecs=opus'
        ],
        qualityPresets: {
            high: {
                sampleRate: 48000,
                bitrate: 192000,
                channels: 2
            },
            medium: {
                sampleRate: 44100,
                bitrate: 160000,
                channels: 2
            },
            standard: {
                sampleRate: 44100,
                bitrate: 128000,
                channels: 1
            }
        }
    },
    
    // UI Configuration
    ui: {
        maxRecordingTime: 300, // 5 minutes in seconds
        showQualityIndicator: true,
        showFileSize: true,
        showDuration: true,
        // Walkie-talkie specific UI settings
        walkieTalkieMode: true,
        pushToTalk: true,
        autoPlayResponses: true,
        showConnectionStatus: true
    },
    
    // Metadata Configuration
    metadata: {
        defaultFullName: 'Anonymous User',
        defaultEmail: 'user@example.com',
        includeTimestamp: true,
        includeSource: true,
        includeAudioQuality: true
    },
    
    // File Configuration
    file: {
        defaultExtension: 'webm',
        maxFileSize: 50 * 1024 * 1024, // 50MB
        allowedTypes: ['audio/webm', 'audio/mp3', 'audio/wav', 'audio/m4a']
    },
    
    // Walkie-talkie Configuration
    walkieTalkie: {
        pollInterval: 2000, // Check for responses every 2 seconds
        maxWaitTime: 30000, // Maximum wait time for response
        connectionTimeout: 5000, // Connection timeout
        retryInterval: 5000, // Retry connection every 5 seconds
        audioBufferSize: 4096, // Audio buffer size for playback
        responseFormats: ['audio/mp3', 'audio/wav', 'audio/webm', 'audio/ogg']
    }
};

// Export for Node.js (if using in Python script)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

// Make available globally for browser
if (typeof window !== 'undefined') {
    window.CONFIG = CONFIG;
}
