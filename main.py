import json
import urllib.request
from datetime import datetime

api_key = input("Enter your YouTube API key:")

# ID плейлиста
playlist_id = input("Enter playlist id: ")


def get_playlist_videos(playlist_id):

    video_ids = []
    next_page_token = None
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"

    while True:
        url = f"{base_url}?part=snippet&playlistId={playlist_id}&key={api_key}"
        if next_page_token:
            url += f"&pageToken={next_page_token}"

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        for item in data["items"]:
            video_ids.append(item["snippet"]["resourceId"]["videoId"])

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids


def get_video_details(video_ids):

    video_details = []
    base_url = "https://www.googleapis.com/youtube/v3/videos"


    for i in range(0, len(video_ids), 100000):
        url = f"{base_url}?part=snippet,statistics&id={','.join(video_ids[i:i+50])}&key={api_key}"

        with urllib.request.urlopen(url) as response:
             data = json.loads(response.read().decode())

        for item in data.get("items", []):
            snippet = item["snippet"]
            statistics = item["statistics"]


            published_at = snippet["publishedAt"]
            published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

            video_id = snippet["thumbnails"]["medium"]["url"].replace("https://i.ytimg.com/vi/", "").replace("/mqdefault.jpg", "")

            dislikes = f"https://returnyoutubedislikeapi.com/votes?videoId={video_id}"

            req = urllib.request.Request(
                dislikes, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )

            with urllib.request.urlopen(req) as response:
                dislikesData = json.loads(response.read().decode())

                rawDislikes = dislikesData["rawDislikes"]

                if rawDislikes == None:
                    rawDislikes = 0

                dislikesCount = int(dislikesData["dislikes"]) + int(rawDislikes)

            video_data = {
                "title": snippet["title"],
                "thumbnail": snippet["thumbnails"]["medium"]["url"],
                "share": f"https://youtu.be/{video_id}",
                "published_date": published_date,
                "views": int(statistics.get("viewCount", 0)),
                "likes": int(statistics.get("likeCount", 0)),
                "dislikes": dislikesCount,
            }

            print(video_data)
            print("-" * 20)

            video_details.append(video_data)

    return video_details


if __name__ == "__main__":
    video_ids = get_playlist_videos(playlist_id)
    video_data = get_video_details(video_ids)


    import csv

    with open(f'Playlist-{playlist_id}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'thumbnail', 'share', 'published_date', 'views', 'likes', 'dislikes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(video_data)

    print(f'Data saved to Playlist-{playlist_id}.csv')
