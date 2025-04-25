# YouTube Video Downloader

This is a simple YouTube video downloader app built using **Streamlit** and **pytubefix**. It allows you to download YouTube videos in both video+audio format or audio-only format.

## Features

- **Scrape YouTube video details** (Title, Description, Thumbnail, Publish Date, Views)
- **Download YouTube videos** in various formats
- **Download Audio-only** or **Video+Audio** formats
- **Progress indicator** showing download status and speed

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/MuhammadTalhaKhalid/youtube_downloader.git
   cd youtube_downloader
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run video_app.py
   ```

## Requirements

The following Python packages are required:

- `streamlit==1.44.1`
- `pytubefix==8.12.3`
- `requests==2.32.3`
- `beautifulsoup4==4.12.3`

