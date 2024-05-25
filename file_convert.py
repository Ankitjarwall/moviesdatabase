import subprocess
import os
import time

# Define the path to the file containing URLs
urls_file_path = "highest_quality_url.txt"
processed_urls = set()

# Define the path to the download directory
download_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', 'movies')

# Create the download directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Function to download video using FFmpeg


def download_video(video_id, m3u8_url):
    output_file = os.path.join(download_dir, f"{video_id}.mp4")
    result = subprocess.run([
        "ffmpeg",
        "-i", m3u8_url,
        "-c", "copy",
        output_file
    ], capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        print(f"Video {video_id} downloaded and saved as {output_file}")
    else:
        print(f"Failed to download video {video_id}. Error: {result.stderr}")


# Main loop to continuously monitor the file
while True:
    if os.path.exists(urls_file_path):
        with open(urls_file_path, "r") as file:
            lines = file.readlines()

        new_lines = [line.strip()
                     for line in lines if line.strip() not in processed_urls]

        if new_lines:
            for line in new_lines:
                # Split the line to get the video ID and URL
                try:
                    print("downloading...")
                    video_id, m3u8_url = line.split(" : ")
                    processed_urls.add(line.strip())
                    download_video(video_id, m3u8_url)
                except ValueError:
                    print(f"Invalid line format: {line}")

        else:
            print("No new URLs found. Waiting for new entries...")
    else:
        print(
            f"File {urls_file_path} not found. Waiting for the file to be created...")

    # Wait for 10 seconds before checking again
    time.sleep(10)
