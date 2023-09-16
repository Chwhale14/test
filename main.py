import requests
from bs4 import BeautifulSoup
import wikipedia
import praw
import os
from googleapiclient.discovery import build
import random
from concurrent.futures import ProcessPoolExecutor
import asyncio

folder_name = "text_files"
api_key = 'AIzaSyDGX7_aYC1wMgv9RpxNcx4xiv2MZMyxz1w'
video_ids = []

reddit = praw.Reddit(
    client_id = "r9JTmSSPLPiUnjr4HKu62w",
    client_secret = "SrYESYhTnIrmM1YrenH3jCK7Hx-OLA",
    user_agent = "Test dataset scraper 1.0 by /u/test_acc69420"
)

youtube = build('youtube', 'v3', developerKey=api_key)

#creating files
def create_file(text):
    pass

#getting posts
def get_wiki_post():
    url = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(id="firstHeading").text
    summary = wikipedia.summary(title)

    return summary

def get_reddit_post():
    random_post = reddit.random_subreddit().random()
    print(random_post.score)
    while random_post.score < 4:
        random_post = reddit.random_subreddit().random()
    
    return random_post.text

def get_youtube_vid():

    request = youtube.search().list(
        part='id',
        type='video',
        maxResults=50,
        q='random',
        relevanceLanguage='en'
    )

    response = request.execute()
    for video in response['items']:
        video_id = video['id']['videoId']
        video_ids.append(video_id)
    
    video_id = random.choice(video_ids)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    description = response['items'][0]['snippet']['description']

    return description
    
async def main(loop):
    tasks = [get_reddit_post, get_wiki_post, get_youtube_vid]
    executor = ProcessPoolExecutor(max_workers=3)
    data = await asyncio.gather(*(loop.run_in_executor(executor, task, num) for task in tasks for num in range(50)))

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))