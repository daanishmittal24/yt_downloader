# import streamlit as st
# import yt_dlp
# import moviepy.editor as mp
# import os
# import zipfile

# # Streamlit interface
# st.title("Video Audio Downloader and Merger")

# search_query = st.text_input("Enter video search query:", "cat funny videos")
# num_videos = st.slider("Number of videos to download:", min_value=1, max_value=10, value=5)
# trim_seconds = st.slider("Seconds to trim from start of each video:", min_value=0, max_value=60, value=10)

# # Temporary output folders
# output_folder = "videos"
# audio_folder = "audio"
# merged_audio_path = os.path.join(audio_folder, "merged_audio.wav")
# zip_file_path = os.path.join(audio_folder, "merged_audio.zip")

# os.makedirs(output_folder, exist_ok=True)
# os.makedirs(audio_folder, exist_ok=True)

# def download_videos(search_query, num_videos):
#     ydl_opts = {
#         'format': 'best[ext=mp4]/best[ext=webm]/best',
#         'noplaylist': True,
#         'max_downloads': num_videos,
#         'quiet': True,
#         'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s')
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download(f"ytsearch{num_videos}:{search_query}")

# def process_audio(trim_seconds):
#     audio_clips = []
#     video_files = [f for f in os.listdir(output_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))]
#     for video_file in video_files:
#         video_path = os.path.join(output_folder, video_file)
#         audio_path = os.path.join(audio_folder, f"{os.path.splitext(video_file)[0]}.wav")
#         video = mp.VideoFileClip(video_path).subclip(trim_seconds)
#         video.audio.write_audiofile(audio_path)
#         audio_clips.append(mp.AudioFileClip(audio_path))
#     return audio_clips

# def merge_audio(audio_clips):
#     merged_audio = mp.concatenate_audioclips(audio_clips)
#     merged_audio.write_audiofile(merged_audio_path)
#     with zipfile.ZipFile(zip_file_path, 'w') as zipf:
#         zipf.write(merged_audio_path, os.path.basename(merged_audio_path))

# if st.button("Download and Process"):
#     with st.spinner("Downloading videos..."):
#         download_videos(search_query, num_videos)
#         st.success(f"Downloaded {num_videos} videos.")
    
#     with st.spinner("Processing audio..."):
#         audio_clips = process_audio(trim_seconds)
#         merge_audio(audio_clips)
#         st.success("Audio processed and merged.")

#     st.audio(merged_audio_path)

#     with open(merged_audio_path, "rb") as audio_file:
#         st.download_button(label="Download Merged Audio", data=audio_file, file_name="merged_audio.wav", mime="audio/wav")


import streamlit as st
import yt_dlp
import moviepy.editor as mp
import os
import zipfile

import streamlit as st
import yt_dlp
import moviepy.editor as mp
import os
import zipfile

# Streamlit interface
st.title("Video Audio Downloader and Merger")

search_query = st.text_input("Enter video search query:", "cat funny videos")
num_videos = st.slider("Number of videos to download:", min_value=1, max_value=10, value=5)
trim_seconds = st.slider("Seconds to trim from start of each video:", min_value=0, max_value=60, value=10)

# Temporary output folders
output_folder = "videos"
audio_folder = "audio"
merged_audio_path = os.path.join(audio_folder, "merged_audio.wav")
zip_file_path = os.path.join(audio_folder, "merged_audio.zip")

os.makedirs(output_folder, exist_ok=True)
os.makedirs(audio_folder, exist_ok=True)

def download_videos(search_query, num_videos):
    ydl_opts = {
        'format': 'best[ext=mp4]/best[ext=webm]/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s')
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{num_videos}:{search_query}", download=False)
        
        # Filter videos shorter than 6 minutes (360 seconds)
        filtered_videos = [entry for entry in search_results['entries'] if entry.get('duration', 0) <= 360]
        
        # Download only the filtered videos
        for video in filtered_videos[:num_videos]:
            ydl.download([video['webpage_url']])
            if len(filtered_videos) >= num_videos:
                break

def process_audio(trim_seconds):
    audio_clips = []
    video_files = [f for f in os.listdir(output_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))]
    
    for video_file in video_files:
        video_path = os.path.join(output_folder, video_file)
        audio_path = os.path.join(audio_folder, f"{os.path.splitext(video_file)[0]}.wav")
        video = mp.VideoFileClip(video_path).subclip(trim_seconds)
        video.audio.write_audiofile(audio_path)
        audio_clips.append(mp.AudioFileClip(audio_path))
    
    return audio_clips

def merge_audio(audio_clips):
    merged_audio = mp.concatenate_audioclips(audio_clips)
    merged_audio.write_audiofile(merged_audio_path)
    
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(merged_audio_path, os.path.basename(merged_audio_path))

if st.button("Download and Process"):
    with st.spinner("Downloading videos..."):
        download_videos(search_query, num_videos)
        st.success(f"Downloaded {num_videos} videos shorter than 6 minutes.")
    
    with st.spinner("Processing audio..."):
        audio_clips = process_audio(trim_seconds)
        merge_audio(audio_clips)
        st.success("Audio processed and merged.")

    st.audio(merged_audio_path)

    with open(merged_audio_path, "rb") as audio_file:
        st.download_button(label="Download Merged Audio", data=audio_file, file_name="merged_audio.wav", mime="audio/wav")
