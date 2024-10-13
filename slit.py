import streamlit as st
import yt_dlp
import moviepy.editor as mp
import os
import zipfile
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

st.title("Video Audio Downloader and Merger")

search_query = st.text_input("Enter video search query:", "Tseries Music")
num_videos = st.slider("Number of videos to download:", min_value=1, max_value=10, value=3)
trim_seconds = st.slider("Seconds to trim from start of each video:", min_value=0, max_value=60, value=5)
email_address = st.text_input("Enter your email address:")

output_folder = "videos"
audio_folder = "audio"
merged_audio_path = os.path.join(audio_folder, "merged_audio.wav")
zip_file_path = os.path.join(audio_folder, "merged_audio.zip")

os.makedirs(output_folder, exist_ok=True)
os.makedirs(audio_folder, exist_ok=True)

def sanitize_filename(filename):
    """Sanitize the filename to remove invalid characters."""
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)  # Remove special characters and control chars
    return sanitized

def download_videos(search_query, num_videos):
    ydl_opts = {
        'format': 'best[ext=mp4]/best[ext=webm]/best',
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
            st.error(f"Error processing {video_file}: {e}")
        finally:
            video.close()
    
    return audio_clips

def merge_audio(audio_clips):
    if audio_clips:
        merged_audio = mp.concatenate_audioclips(audio_clips)
        merged_audio.write_audiofile(merged_audio_path)
        
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            zipf.write(merged_audio_path, os.path.basename(merged_audio_path))
        
        for audio_clip in audio_clips:
            audio_clip.close()

def delete_files():
    video_files = [f for f in os.listdir(output_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))]
    for video_file in video_files:
        video_path = os.path.join(output_folder, video_file)
        os.remove(video_path) 
    
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.wav') and f != 'merged_audio.wav']
    for audio_file in audio_files:
        audio_path = os.path.join(audio_folder, audio_file)
        os.remove(audio_path)  
    
    st.success("Video and individual audio files have been deleted.")

def send_email(recipient_email):
    """Send the merged audio file to the specified email."""
    sender_email = "mrolaf2403@gmail.com"  # Your email address
    sender_password = "271172"  # Your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your Merged Audio File"
    
    body = "Please find the attached merged audio file."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the audio file
    with open(merged_audio_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(merged_audio_path)}",
        )
        msg.attach(part)

    # Sending the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.send_message(msg)

if st.button("Download and Process"):
    with st.spinner("Downloading videos..."):
        download_videos(search_query, num_videos)
        st.success(f"Downloaded {num_videos} videos.")
    
    with st.spinner("Processing audio..."):
        audio_clips = process_audio(trim_seconds)
        merge_audio(audio_clips)
        st.success("Audio processed and merged.")

    st.audio(merged_audio_path)

    with open(merged_audio_path, "rb") as audio_file:
        st.download_button(label="Download Merged Audio", data=audio_file, file_name="merged_audio.wav", mime="audio/wav")
    
    if email_address:
        with st.spinner("Sending email..."):
            send_email(email_address)
            st.success(f"Merged audio sent to {email_address}.")
    
    delete_files()

st.markdown("""
    <br><br>
    <h5 style='text-align: center;'>Made with ❤️ by <a href='https://github.com/daanishmittal24' target='_blank'> Daanish Mittal<br></a></h5>
""", unsafe_allow_html=True)
