#!/usr/bin/env python3
"""
Simple test for YouTube2Post functionality
This script simulates what the n8n workflow would do
"""

import os
import subprocess
import json
import sys
import tempfile
from datetime import datetime

def download_video_info(youtube_url):
    """Get video information using yt-dlp"""
    print(f"📥 Getting video info for: {youtube_url}")

    try:
        # Get video info without downloading
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--no-download',
            youtube_url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"❌ Error getting video info: {result.stderr}")
            return None

        video_info = json.loads(result.stdout)

        return {
            'title': video_info.get('title', 'Unknown'),
            'channel': video_info.get('channel', 'Unknown'),
            'duration': video_info.get('duration', 0),
            'description': video_info.get('description', '')[:200],
            'thumbnail': video_info.get('thumbnail', ''),
            'url': youtube_url,
            'id': video_info.get('id', '')
        }

    except subprocess.TimeoutExpired:
        print("❌ Timeout getting video info")
        return None
    except json.JSONDecodeError:
        print("❌ Failed to parse video info")
        return None
    except FileNotFoundError:
        print("❌ yt-dlp not found. Please install it: pip install yt-dlp")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def download_video_with_subtitle(youtube_url, output_dir="/tmp"):
    """Download video and subtitles"""
    print(f"📥 Downloading video and subtitles...")

    video_id = youtube_url.split('/')[-1].split('?')[0]
    output_path = os.path.join(output_dir, f"{video_id}")

    try:
        # Download video with subtitles
        cmd = [
            'yt-dlp',
            '--write-auto-sub',
            '--sub-lang', 'zh,en',
            '--convert-subs', 'srt',
            '--output', f'{output_path}.%(ext)s',
            '--format', 'worst[ext=mp4]/worst',  # Get smallest version for testing
            '--no-playlist',
            youtube_url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            print(f"⚠️ Download warning: {result.stderr}")

        # Check what files were created
        import glob
        files = glob.glob(f"{output_path}*")

        return {
            'video_file': f"{output_path}.mp4" if os.path.exists(f"{output_path}.mp4") else None,
            'subtitle_files': [f for f in files if '.srt' in f],
            'all_files': files
        }

    except subprocess.TimeoutExpired:
        print("❌ Timeout downloading video")
        return None
    except FileNotFoundError:
        print("❌ yt-dlp not found")
        return None
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None

def extract_text_from_subtitles(subtitle_file):
    """Extract text from SRT file"""
    if not subtitle_file or not os.path.exists(subtitle_file):
        return None

    try:
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        text_lines = []
        for line in lines:
            line = line.strip()
            # Skip timecodes and numbers
            if '-->' not in line and line and not line.isdigit():
                text_lines.append(line)

        return ' '.join(text_lines)
    except Exception as e:
        print(f"❌ Error reading subtitles: {e}")
        return None

def simulate_quote_extraction(text):
    """Simulate AI quote extraction"""
    if not text:
        return []

    # For demo, extract first few sentences as "quotes"
    sentences = text.split('.')[:5]

    quotes = []
    for i, sentence in enumerate(sentences):
        if len(sentence.strip()) > 10:  # Skip very short sentences
            quotes.append({
                'text': sentence.strip() + '.',
                'timestamp': f"00:00:{(i+1)*10:02d}",
                'importance': 'high' if i < 2 else 'medium'
            })

    return quotes[:3]  # Return top 3 quotes

def process_youtube_shorts(url):
    """Main processing function for YouTube Shorts"""
    print("🚀 Starting YouTube Shorts processing...")
    print(f"📹 URL: {url}\n")

    # Step 1: Get video info
    video_info = download_video_info(url)
    if not video_info:
        return {'success': False, 'error': 'Failed to get video info'}

    print(f"✅ Video Title: {video_info['title']}")
    print(f"✅ Channel: {video_info['channel']}")
    print(f"✅ Duration: {video_info['duration']} seconds\n")

    # Step 2: Download video and subtitles
    download_result = download_video_with_subtitle(url)
    if not download_result:
        return {'success': False, 'error': 'Failed to download video'}

    print(f"✅ Downloaded files: {len(download_result['all_files'])} files")

    # Step 3: Extract text from subtitles
    text = None
    if download_result['subtitle_files']:
        subtitle_file = download_result['subtitle_files'][0]
        print(f"📝 Processing subtitle: {subtitle_file}")
        text = extract_text_from_subtitles(subtitle_file)

    if not text:
        print("⚠️ No subtitles found, using video description")
        text = video_info['description']

    # Step 4: Extract quotes
    quotes = simulate_quote_extraction(text)
    print(f"\n💎 Extracted {len(quotes)} quotes:")
    for i, quote in enumerate(quotes, 1):
        print(f"  {i}. {quote['text'][:50]}...")

    # Step 5: Generate result
    result = {
        'success': True,
        'taskId': f"youtube2post_{video_info['id']}",
        'video': video_info,
        'quotes': quotes,
        'transcription': text[:500] if text else "No transcription available",
        'files': download_result,
        'processedAt': datetime.now().isoformat(),
        'message': f"Successfully processed YouTube Shorts: {video_info['title']}"
    }

    # Clean up large files from result for display
    if 'files' in result:
        result['files'] = {
            'count': len(result['files'].get('all_files', [])),
            'has_video': bool(result['files'].get('video_file')),
            'has_subtitles': bool(result['files'].get('subtitle_files'))
        }

    return result

def main():
    """Test with the provided YouTube Shorts URL"""
    youtube_url = "https://youtube.com/shorts/rLhoe1ZjW-s"

    print("=" * 60)
    print("🎬 YouTube2Post Test Script")
    print("=" * 60 + "\n")

    result = process_youtube_shorts(youtube_url)

    print("\n" + "=" * 60)
    print("📊 Final Result:")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result['success']:
        print("\n✅ Test completed successfully!")
        print(f"\n📝 Summary:")
        print(f"  - Video: {result['video']['title'][:50]}...")
        print(f"  - Quotes extracted: {len(result['quotes'])}")
        print(f"  - Files processed: {result['files']['count']}")
    else:
        print(f"\n❌ Test failed: {result.get('error', 'Unknown error')}")

    return 0 if result['success'] else 1

if __name__ == "__main__":
    sys.exit(main())