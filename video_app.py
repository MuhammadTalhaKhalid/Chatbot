import streamlit as st
from pytubefix import YouTube
import requests
from bs4 import BeautifulSoup
import os
import time
import streamlit
import pytubefix
import bs4

print("streamlit:", streamlit.__version__)
print("pytubefix:", pytubefix.__version__)
print("requests:", requests.__version__)
print("beautifulsoup4:", bs4.__version__)

# Page setup
st.set_page_config(page_title="YouTube Downloader", layout="wide")

# Background and styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1518770660439-4636190af475");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 15px;
    }
    .stTextInput > div > div > input {
        background-color: #f0f4f8;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #1E90FF;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 10px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #4169E1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📽️ YouTube Scraper + Downloader ")

def scrape_youtube_video_details(video_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(video_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find("meta", property="og:title")["content"]
        description = soup.find("meta", property="og:description")["content"]
        thumbnail = soup.find("meta", property="og:image")["content"]

        date_tag = soup.find("meta", itemprop="datePublished")
        view_tag = soup.find("meta", itemprop="interactionCount")

        publish_date = date_tag["content"] if date_tag else "N/A"
        views = f"{int(view_tag['content']):,}" if view_tag else "N/A"

        return {
            "title": title,
            "description": description,
            "thumbnail": thumbnail,
            "publish_date": publish_date,
            "views": views
        }
    except Exception as e:
        return {"error": str(e)}

def download_youtube_video(video_url, audio_only=False, progress_callback=None):
    try:
        start_time = time.time()
        downloaded_bytes = [0]

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            downloaded_bytes[0] = bytes_downloaded
            if progress_callback:
                elapsed = time.time() - start_time
                speed = downloaded_bytes[0] / elapsed if elapsed > 0 else 0
                progress_callback(bytes_downloaded, total_size, speed)

        yt = YouTube(video_url, on_progress_callback=on_progress)

        if audio_only:
            stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            file = stream.download(output_path="downloads/", filename_prefix="audio_")
        else:
            video_stream = yt.streams.filter(file_extension='mp4', only_video=True).order_by('resolution').desc().first()
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            video_file = video_stream.download(output_path="downloads/", filename_prefix="video_")
            audio_file = audio_stream.download(output_path="downloads/", filename_prefix="audio_")
            title = "".join(c for c in yt.title if c.isalnum() or c in (' ', '.', '_')).rstrip()
            combined_file = f"downloads/{title}_combined.mp4"
            os.system(f"ffmpeg -y -i \"{video_file}\" -i \"{audio_file}\" -c:v copy -c:a aac \"{combined_file}\"")
            os.remove(video_file)
            os.remove(audio_file)
            file = combined_file

        size = os.path.getsize(file) / (1024 * 1024)
        return file, f"{size:.2f} MB"
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# Interface
url = st.text_input("🔗 Enter YouTube Video URL")

video_path = None
file_size = None

col1, col2 = st.columns(2)

with col1:
    if "youtube.com/watch?v=" in url:
        st.info("Fetching video metadata...")
        info = scrape_youtube_video_details(url)
        if "error" in info:
            st.error(info['error'])
        else:
            st.subheader("🎬 Title")
            st.write(info["title"])
            st.subheader("📜 Description")
            st.write(info["description"])
            st.image(info["thumbnail"], width=400)
            st.write(f"📅 Published: {info['publish_date']}")
            st.write(f"👁️ Views: {info['views']}")

with col2:
    download_type = st.radio("Choose download type", ["🎥 Video + Audio", "🎧 Audio Only"])
    if st.button("⬇️ Download"):
        if "youtube.com/watch?v=" not in url:
            st.error("❌ Invalid YouTube URL.")
        else:
            st.info("Downloading...")
            progress = st.progress(0)
            progress_text = st.empty()

            def progress_callback(downloaded, total, speed):
                percent = int(downloaded * 100 / total)
                mb_downloaded = downloaded / (1024 * 1024)
                mb_total = total / (1024 * 1024)
                progress.progress(percent)
                progress_text.markdown(
                    f"📦 **Downloaded:** {mb_downloaded:.2f} MB / {mb_total:.2f} MB  \n🚀 **Speed:** {speed / (1024 * 1024):.2f} MB/s"
                )

            is_audio = download_type == "🎧 Audio Only"
            result, size = download_youtube_video(url, audio_only=is_audio, progress_callback=progress_callback)

            if "downloads/" in result:
                st.success("✅ Download complete!")
                st.write(f"📁 File: `{result}`")
                st.write(f"💾 Size: {size}")
                video_path = result
                file_size = size
            else:
                st.error(result)

if video_path and not video_path.endswith(".mp3") and os.path.exists(video_path):
    st.subheader("▶️ Play Downloaded Video")
    st.video(video_path)
