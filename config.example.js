// Example Configuration File for Audio Transcription Project
// Copy this file to config.js and modify the values as needed

const CONFIG = {
    // Webhook Configuration
    webhook: {
        // Change this to your actual n8n webhook URL
        url: 'https://your-n8n-instance.com/webhook/audio-webhook',
        timeout: 30000, // 30 seconds timeout
        retryAttempts: 3
    },
    
    // Audio Recording Configuration
    audio: {
        // Professional quality settings
        defaultSampleRate: 48000,        // 48kHz for professional quality
        defaultBitrate: 192000,          // 192kbps for high quality
        defaultChannels: 2,              // Stereo recording
        
        // Supported audio formats (in order of preference)
        supportedFormats: [
            'audio/webm;codecs=opus;rate=48000',  // Best quality
            'audio/webm;codecs=opus;rate=44100',  // Good quality
            'audio/webm;codecs=opus'              // Standard quality
        ],
        
        // Quality presets for different use cases
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
        maxRecordingTime: 300,           // 5 minutes in seconds
        showQualityIndicator: true,      // Show audio quality info
        showFileSize: true,              // Show file size
        showDuration: true               // Show recording duration
    },
    
    // Metadata Configuration
    metadata: {
        defaultFullName: 'Anonymous User',           // Default full name
        defaultEmail: 'user@example.com',            // Default email
        includeTimestamp: true,                      // Include timestamp
        includeSource: true,                         // Include source info
        includeAudioQuality: true                    // Include quality info
    },
    
    // File Configuration
    file: {
        defaultExtension: 'webm',                      // Default file extension
        maxFileSize: 50 * 1024 * 1024,                // 50MB max file size
        allowedTypes: ['audio/webm', 'audio/mp3', 'audio/wav', 'audio/m4a']
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
