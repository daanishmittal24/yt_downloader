# Video Audio Downloader and Merger

This Streamlit application allows users to search for videos, download them, extract and merge their audio, and provide an option to download the merged audio as a zip file. 

## Features
- **Search for Videos**: Enter a search query to find videos on platforms supported by `yt-dlp`.
- **Download Videos**: Download multiple videos based on the search query.
- **Audio Processing**: Trim the beginning of each video and extract the audio.
- **Merge Audio**: Merge all extracted audio clips into a single audio file.
- **Download Merged Audio**: Easily download the merged audio file.
- **File Management**: Automatically delete downloaded video files and individual audio files after processing.

## Prerequisites

Before running the application, ensure you have the following installed:
- Python 3.7 or later
- Streamlit
- yt-dlp
- moviepy
- other dependencies

You can install the required packages using pip:

```bash
pip install streamlit yt-dlp moviepy
```

## Usage

1. **Clone this Repository** (if applicable):

   ```bash
   git clone https://github.com/your_username/video-audio-downloader.git
   cd video-audio-downloader
   ```

2. **Run the Application**:

   Execute the following command in your terminal:

   ```bash
   streamlit run app.py
   ```

   Replace `app.py` with the name of your main Python script if different.

3. **Interact with the Application**:

   - Open your web browser and go to `http://localhost:8501` (or the address provided in your terminal).
   - Enter a search query in the input box (e.g., "Tseries Music").
   - Adjust the slider to select the number of videos you want to download.
   - Set the number of seconds to trim from the start of each video.
   - Click the "Download and Process" button to begin.

4. **Download Merged Audio**: 
   - After processing, you can listen to the merged audio and download it using the provided button.

## File Management
- The application will automatically delete the downloaded video files and individual audio files, leaving only the merged audio file.

## Error Handling
- The application includes error handling to catch and display any issues encountered during the download or audio processing phases.

## Limitations
- Ensure you have a stable internet connection for downloading videos.
- Some video formats may not be supported for audio extraction.

## Author
Made by Daanish Mittal.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading functionality.
- [MoviePy](https://zulko.github.io/moviepy/) for audio processing.
