import yt_dlp
import os
import moviepy.editor as mp
import re
import zipfile

output_folder = "videos"
audio_folder = "audio"
merged_audio_path = os.path.join(audio_folder, "merged_audio.mp3")

os.makedirs(output_folder, exist_ok=True)
os.makedirs(audio_folder, exist_ok=True)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)

def download_videos(search_query, num_videos):
    ydl_opts = {
        'format': 'worst[ext=mp4]/worst[ext=webm]/worst',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s')
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{search_query}"])

def process_audio(trim_seconds):
    audio_clips = []
    video_files = [f for f in os.listdir(output_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))]
    
    for video_file in video_files:
        video_path = os.path.join(output_folder, video_file)
        audio_filename = sanitize_filename(f"{os.path.splitext(video_file)[0]}.wav")
        audio_path = os.path.join(audio_folder, audio_filename)
        
        try:
            video = mp.VideoFileClip(video_path).subclip(trim_seconds)
            video.audio.write_audiofile(audio_path)
            audio_clips.append(mp.AudioFileClip(audio_path))
        except Exception as e:
            print(f"Error processing {video_file}: {e}")
        finally:
            video.close()
    
    return audio_clips

def merge_audio(audio_clips):
    if audio_clips:
        merged_audio = mp.concatenate_audioclips(audio_clips)
        merged_audio.write_audiofile(merged_audio_path, codec='mp3', bitrate='64k')
        
        for audio_clip in audio_clips:
            audio_clip.close()

def delete_files():
    for video_file in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, video_file))
    
    for audio_file in os.listdir(audio_folder):
        if audio_file != 'merged_audio.mp3':
            os.remove(os.path.join(audio_folder, audio_file))

if __name__ == "__main__":
    search_query = input("Enter the search query: ")
    num_videos = int(input("Enter the number of videos to download: "))
    trim_seconds = int(input("Enter the seconds to trim from the start of each video: "))

    print("Downloading videos...")
    download_videos(search_query, num_videos)
    
    print("Processing audio...")
    audio_clips = process_audio(trim_seconds)
    
    print("Merging audio...")
    merge_audio(audio_clips)
    
    print(f"Merged audio saved at: {merged_audio_path}")
    
    delete_files()

