
# Video Audio Downloader and Merger
## Deployed Application
You can access the deployed application at: [Video Audio Downloader and Merger](https://youtube-downloader-merge.streamlit.app)

## Description
This application allows users to search for videos on YouTube, download a specified number of videos, trim the audio from the beginning, and merge the audio into a single file.

![image](https://github.com/user-attachments/assets/e912b4f0-0b05-4acd-bbaf-d12047d0056f)


## Features
- Search for videos on YouTube based on a query.
- Download multiple videos at once.
- Trim the beginning of the audio from each video.
- Merge the audio files into a single output file.
- Download the merged audio file.
- User-friendly interface using Streamlit.

## Requirements
- Python 3.x
- yt-dlp
- moviepy
- Streamlit

## Installation
1. Clone this repository or download the code.
2. Install the required packages:
    ```bash
    pip install yt-dlp moviepy streamlit
    ```
3. Run the application:
    ```bash
    streamlit run app.py
    ```

## Usage
1. Enter the video search query.
2. Adjust the number of videos to download.
3. Set the seconds to trim from the start of each video.
4. Click on **Download and Process** to start downloading and processing.
5. Listen to the merged audio and download it if desired.


## License
This project is open-source and available for modification and redistribution.
