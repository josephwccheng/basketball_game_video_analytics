from dotenv import load_dotenv
import os
import logging
import youtube_extractor
import json

def setup_tokens():
    expected_env_vars = [
        'YOUTUBE_DOWNLOAD',
        'VIDEO_PATH'
    ]
    # Refresh environment variables since load_dotenv doesn't override them if already set
    for env_var in expected_env_vars:
        if os.getenv(env_var) is not None:
            del os.environ[env_var]
            logging.info('Refreshed environment variable: {}'.format(env_var))

    # Load environment variables saved in .env file
    load_dotenv()
    for env_var in expected_env_vars:
        if os.getenv(env_var) is None:
            raise ValueError(
                '.env file is missing or {} has not been defined in the .env file'.format(
                    env_var)
            )

# Step 1. Downloading Videos (Only Required once per video)
def download_videos():
    with open('games.json') as json_file:
        data = json.load(json_file)
    ytExtractor = youtube_extractor.YoutubeExtractor()
    ytExtractor.download(data[0]['url'])

def main():
    setup_tokens()
    # Step 1: Download videos only if the youtube download environment variable is true
    if os.getenv('YOUTUBE_DOWNLOAD').lower() == "true":
        download_videos()
    else:
        print("skipping video download")
    
    # Step 2: Read the video from the .data folder
    video_lists = os.listdir(os.getenv('VIDEO_PATH'))
    if len(video_lists) < 0:
        print("no videos in .data folder")
    else:
        print(f"first video is: {video_lists[0]}")
main()