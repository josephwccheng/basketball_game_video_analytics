from dotenv import load_dotenv
import os
import logging
import youtube_extractor
import json

def setup_tokens():
    expected_env_vars = [
        'YOUTUBE_URL'
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
    download_videos()
    print("main finished")

main()