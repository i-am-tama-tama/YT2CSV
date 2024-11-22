# YouTube Playlist Data Extraction Tool

This project provides a Python script to extract data from a YouTube playlist. It uses the YouTube Data API to fetch video details such as title, publication date, views, likes, and dislikes. Dislikes are retrieved through an additional third-party service, which is **not officially supported by YouTube**, and might be considered illegal.

## Features

- Extracts data from all videos in a given YouTube playlist.
- Retrieves and displays the following video details:
  - Title
  - Thumbnail URL
  - Shareable video link
  - Publication date
  - View count
  - Like count
  - Dislike count (using a third-party API)
- Saves the extracted data to a CSV file.

## Prerequisites

To run this script, you need:

- **Python 3.6+**
- A valid **YouTube Data API key** (refer to [YouTube Data API Documentation](https://developers.google.com/youtube/v3/getting-started) to generate a key).

## Installation

1. **Clone the repository** (or copy the script) to your local machine.
2. **Install dependencies** (if necessary):
   - No external dependencies are required as the script only uses Python's built-in libraries: `json`, `urllib.request`, `datetime`, and `csv`.

## Usage

1. **Obtain a YouTube API Key**:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the **YouTube Data API v3**.
   - Generate an API key for the project.

2. **Run the Script**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Run the script using the command:
     ```bash
     python script_name.py
     ```
   - Enter your **YouTube API key** and the **playlist ID** when prompted.

## How It Works

### Step-by-Step Process

1. **Extract Playlist Video IDs**:
   - The function `get_playlist_videos` takes a playlist ID and retrieves all video IDs associated with that playlist using the YouTube Data API.
   - It handles pagination using the `nextPageToken` to ensure all videos in the playlist are fetched.

2. **Fetch Video Details**:
   - The `get_video_details` function uses the video IDs to get detailed information for each video.
   - The details include the title, thumbnail URL, shareable link, publication date, view count, and like count.
   - The script also retrieves the **dislike count** using a third-party API called **Return YouTube Dislike API**, which scrapes data that is no longer available through YouTube's official API.

3. **Save Data to CSV**:
   - The extracted data is saved to a CSV file named `Playlist-{playlist_id}.csv`, where `{playlist_id}` is the ID of the playlist.
   - Each row in the CSV represents a video's details.

### Script Parameters

- `playlist_id`: The ID of the YouTube playlist to be analyzed.
- `api_key`: Your unique YouTube API key.

### Example Output

After running the script, a CSV file will be generated with the following columns:

| title        | thumbnail                             | share              | published_date | views | likes | dislikes |
|--------------|--------------------------------------|--------------------|----------------|-------|-------|----------|
| Video Title  | URL to video thumbnail                | YouTube short link | Date Published | 12345 | 678   | 90       |

## Disclaimers

- **YouTube API Limitations**: The script may hit request quotas set by the YouTube Data API, so consider monitoring your API usage.
- **Use of Dislike Data**: The `Return YouTube Dislike API` is a third-party service that retrieves dislike data for videos. This API **scrapes YouTube data**, which violates YouTube's terms of service. Using this API **is illegal**, and the author of this script does not endorse or encourage its use.

## Limitations

- The YouTube Data API may not provide all available data due to privacy settings or API restrictions.
- The script is dependent on the availability of the third-party dislike API. If the service is unavailable or banned, dislike data cannot be retrieved.
- Since YouTube removed public dislike counts, the accuracy and legality of retrieving this data through third-party APIs are questionable.

## References

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3/docs)
- [Return YouTube Dislike API](https://returnyoutubedislike.com/) (for retrieving dislike counts)

## License

This script is intended for educational purposes only. Use it at your own risk. The author is not responsible for any misuse or legal issues that arise from using the script. Always comply with YouTube's terms of service when accessing their data.
