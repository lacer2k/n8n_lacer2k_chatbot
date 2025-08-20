# Configuration file for Audio Transcription Project
# Modify these settings as needed

# Webhook Configuration
WEBHOOK_CONFIG = {
    'url': 'https://lacer2k.app.n8n.cloud/webhook-test/b533d79f-b898-40da-ac8d-61039df6dce0',
    'timeout': 30,  # 30 seconds timeout
    'retry_attempts': 3,
    'max_file_size': 50 * 1024 * 1024  # 50MB
}

# Audio Processing Configuration
AUDIO_CONFIG = {
    'supported_formats': ['.mp3', '.wav', '.m4a', '.webm', '.ogg'],
    'max_duration': 300,  # 5 minutes in seconds
    'quality_presets': {
        'high': {
            'sample_rate': 48000,
            'bitrate': 192000,
            'channels': 2
        },
        'medium': {
            'sample_rate': 44100,
            'bitrate': 160000,
            'channels': 2
        },
        'standard': {
            'sample_rate': 44100,
            'bitrate': 128000,
            'channels': 1
        }
    }
}

# File Handling Configuration
FILE_CONFIG = {
    'temp_directory': './temp',
    'cleanup_after_upload': True,
    'allowed_extensions': ['.mp3', '.wav', '.m4a', '.webm', '.ogg', '.flac'],
    'max_filename_length': 255
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'audio_transcription.log'
}

# Metadata Configuration
METADATA_CONFIG = {
    'default_tags': ['voice', 'recording'],
    'default_description': 'Audio recording',
    'include_timestamp': True,
    'include_source': True,
    'include_file_info': True
}
