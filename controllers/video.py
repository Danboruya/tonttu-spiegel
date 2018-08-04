from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import argparse

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_url(cmd):
    search_word = cmd

    argparser = argparse.ArgumentParser(conflict_handler='resolve')
    argparser.add_argument("--q", help="Search term", default=search_word)
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()
    url = "sample"
    try:
        url = {'value': [youtube_search(args)]}
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    return url


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    url = ""
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            url = "" + search_result["id"]["videoId"]
            break

    return url
