#!/usr/bin/env python3
"""
Audio Transcription Script
Downloads audio from a URL and sends it to a webhook for transcription by OpenAI
"""

import requests
import argparse
import os
import sys
from urllib.parse import urlparse
import mimetypes

# Import configuration
try:
    from config import WEBHOOK_CONFIG, AUDIO_CONFIG, FILE_CONFIG, METADATA_CONFIG
except ImportError:
    print("Warning: config.py not found, using default values")
    # Fallback configuration if config.py is not available
    WEBHOOK_CONFIG = {
        'url': 'https://lacer2k.app.n8n.cloud/webhook-test/b533d79f-b898-40da-ac8d-61039df6dce0',
        'timeout': 30,
        'retry_attempts': 3,
        'max_file_size': 50 * 1024 * 1024
    }
    AUDIO_CONFIG = {'supported_formats': ['.mp3', '.wav', '.m4a', '.webm', '.ogg']}
    FILE_CONFIG = {'cleanup_after_upload': True}
    METADATA_CONFIG = {'default_tags': ['voice', 'recording']}

def download_audio(url, output_path=None):
    """
    Download audio file from URL
    """
    try:
        print(f"Downloading audio from: {url}")
        
        # Send request with stream=True for large files
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Determine filename if not provided
        if not output_path:
            # Try to get filename from URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # If no filename in URL, try to get from Content-Disposition header
            if not filename or '.' not in filename:
                content_disposition = response.headers.get('Content-Disposition')
                if content_disposition:
                    # Extract filename from Content-Disposition header
                    import re
                    match = re.search(r'filename="?([^"]+)"?', content_disposition)
                    if match:
                        filename = match.group(1)
                
                # If still no filename, use default
                if not filename or '.' not in filename:
                    # Try to determine extension from content type
                    content_type = response.headers.get('Content-Type', '')
                    if 'audio' in content_type:
                        if 'mp3' in content_type:
                            filename = 'audio.mp3'
                        elif 'wav' in content_type:
                            filename = 'audio.wav'
                        elif 'm4a' in content_type:
                            filename = 'audio.m4a'
                        else:
                            filename = 'audio.audio'
                    else:
                        filename = 'audio.audio'
            
            output_path = filename
        
        # Download the file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Audio downloaded successfully to: {output_path}")
        return output_path
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading audio: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def send_to_webhook(audio_file_path, webhook_url=None):
    """
    Send audio file to webhook for transcription
    """
    try:
        # Use config webhook URL if none provided
        if webhook_url is None:
            webhook_url = WEBHOOK_CONFIG['url']
            
        print(f"Sending audio file to webhook: {webhook_url}")
        
        # Check if file exists
        if not os.path.exists(audio_file_path):
            print(f"Error: Audio file not found: {audio_file_path}")
            return False
        
        # Check file size against config limit
        file_size = os.path.getsize(audio_file_path)
        if file_size > WEBHOOK_CONFIG['max_file_size']:
            print(f"Error: File too large ({file_size / (1024*1024):.1f} MB). Max allowed: {WEBHOOK_CONFIG['max_file_size'] / (1024*1024):.1f} MB")
            return False
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(audio_file_path)
        if not mime_type or not mime_type.startswith('audio/'):
            print(f"Warning: File may not be an audio file. MIME type: {mime_type}")
        
        # Get the filename from the path
        filename = os.path.basename(audio_file_path)
        
        # Prepare the file for upload
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                # IMPORTANT: The field name must match the filename for n8n binary property
                # This ensures the webhook creates the correct binary property structure
                filename: (filename, audio_file, mime_type or 'audio/mpeg')
            }
            
            print(f"Uploading file '{filename}' with field name '{filename}'")
            print(f"File size: {file_size / 1024:.1f} KB")
            print(f"MIME type: {mime_type or 'audio/mpeg'}")
            
            # Send POST request to webhook with config timeout
            response = requests.post(webhook_url, files=files, timeout=WEBHOOK_CONFIG['timeout'])
            
            if response.status_code == 200:
                print("Audio sent successfully to webhook!")
                print(f"Response: {response.text}")
                return True
            else:
                print(f"Error sending to webhook. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"Error sending to webhook: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Download audio from URL and send to webhook for transcription'
    )
    parser.add_argument('url', help='URL of the audio file to download')
    parser.add_argument(
        '--output', '-o', 
        help='Output filename for downloaded audio (optional)'
    )
    parser.add_argument(
        '--webhook', '-w',
        default=WEBHOOK_CONFIG['url'],
        help=f'Webhook URL for transcription (default: {WEBHOOK_CONFIG["url"]})'
    )
    parser.add_argument(
        '--keep-file', '-k',
        action='store_true',
        help='Keep the downloaded audio file after sending to webhook'
    )
    
    args = parser.parse_args()
    
    # Download audio
    audio_file = download_audio(args.url, args.output)
    if not audio_file:
        print("Failed to download audio. Exiting.")
        sys.exit(1)
    
    # Send to webhook
    success = send_to_webhook(audio_file, args.webhook)
    
    # Clean up if requested and configured
    if not args.keep_file and success and FILE_CONFIG['cleanup_after_upload']:
        try:
            os.remove(audio_file)
            print(f"Cleaned up temporary file: {audio_file}")
        except Exception as e:
            print(f"Warning: Could not remove temporary file {audio_file}: {e}")
    
    if success:
        print("Process completed successfully!")
        sys.exit(0)
    else:
        print("Process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
