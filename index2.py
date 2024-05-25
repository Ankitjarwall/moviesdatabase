import csv
import requests
from urllib.parse import urljoin

# Define the paths to the CSV files
csv_file_path = "movies_id.csv"
failed_csv_path = "failed_id.csv"

# Function to update the movies_id.csv file


def update_csv_file(csv_file_path, video_id, status):
    lines = []
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == video_id:
                # Update the status only if it's not already present
                if len(row) == 1 or (len(row) > 1 and row[1] not in ["done", "fail"]):
                    row.append(status)
            lines.append(row)

    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(lines)

# Function to append to the failed_id.csv file


def append_to_failed_csv(failed_csv_path, video_id):
    with open(failed_csv_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([video_id, "fail"])


# Open and read the CSV file
with open(csv_file_path, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    row_count = 0
    for row in csvreader:
        video_id = row[0]

        # Skip if the video ID is already marked as "done" or "fail"
        if len(row) > 1 and row[1] in ["done", "fail"]:
            continue

        # Request the JSON data from the API
        response = requests.get(
            f"https://dl.vidsrc.vip/api/vto/{video_id}.json")

        # Check if the request was successful
        if response.status_code == 200:
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                print(
                    f"Error decoding JSON for video ID {video_id}. Response content: {response.text}")
                update_csv_file(csv_file_path, video_id, "fail")
                append_to_failed_csv(failed_csv_path, video_id)
                continue

            # Extract the Vidplay stream URL
            vidplay_stream_url = None
            for source in data.get("sources", []):
                if source["name"] == "Vidplay":
                    vidplay_stream_url = source["data"]["stream"]
                    break

            # If Vidplay stream URL is found
            if vidplay_stream_url:
                # Download the m3u8 playlist file
                playlist_response = requests.get(vidplay_stream_url)

                # Check if the playlist request was successful
                if playlist_response.status_code == 200:
                    playlist_content = playlist_response.text

                    # Parse the playlist to find the highest quality link
                    highest_quality_url = None
                    highest_bandwidth = 0
                    base_url = vidplay_stream_url.rsplit('/', 1)[0] + '/'
                    lines = playlist_content.splitlines()
                    for i in range(len(lines)):
                        if lines[i].startswith("#EXT-X-STREAM-INF"):
                            # Extract the bandwidth value from the line
                            bandwidth_str = lines[i].split("BANDWIDTH=")[
                                1].split(",")[0]
                            bandwidth = int(bandwidth_str)
                            # Get the URL of the stream variant
                            stream_url = lines[i + 1]
                            # Check if this is the highest bandwidth found so far
                            if bandwidth > highest_bandwidth:
                                highest_bandwidth = bandwidth
                                highest_quality_url = stream_url

                    # Save the highest quality URL to a file
                    if highest_quality_url:
                        full_url = urljoin(base_url, highest_quality_url)
                        with open("highest_quality_url.txt", "a") as file:  # Open in append mode
                            file.write(f"{video_id} : {full_url}\n")
                        print(
                            f"Highest quality URL for {video_id} appended to highest_quality_url.txt")
                        update_csv_file(csv_file_path, video_id, "done")
                    else:
                        print(
                            f"No valid stream URL found in the playlist for {video_id}.")
                        update_csv_file(csv_file_path, video_id, "fail")
                        append_to_failed_csv(failed_csv_path, video_id)
                else:
                    print(
                        f"Failed to download playlist for video ID {video_id}. Status code: {playlist_response.status_code}")
                    update_csv_file(csv_file_path, video_id, "fail")
                    append_to_failed_csv(failed_csv_path, video_id)
            else:
                print(f"Vidplay stream URL not found for {video_id}.")
                update_csv_file(csv_file_path, video_id, "fail")
                append_to_failed_csv(failed_csv_path, video_id)
        else:
            print(
                f"Failed to fetch data for video ID {video_id}. Status code: {response.status_code}")
            update_csv_file(csv_file_path, video_id, "fail")
            append_to_failed_csv(failed_csv_path, video_id)

        # Increment the row count and break if the limit is reached
        row_count += 100000
        if row_count >= 200000:
            break
