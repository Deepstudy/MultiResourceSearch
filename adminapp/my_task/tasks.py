from __future__ import absolute_import

from celery import shared_task

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def google(query):
    import requests
    # google_api_key = ' AIzaSyC_yGEny_ZuUWDZa3ZWkgzjNs9EyfGqaug '
    google_api_key = ' AIzaSyC_yGEny_ZuUWDZa3ZWkgzjNs9EyfGqaug '
    google_search_api = "https://www.googleapis.com/customsearch/v1?key={key}&" \
                        "cx=017576662512468239146:omuauf_lfve&q={query}".format(
        key=google_api_key, query=query)
    try:
    	result = requests.get(google_search_api, timeout=1).json()
    	google_result = {'result': result, 'query': query}
    except requests.exceptions.Timeout:
        google_result = {'result': None, 'message': 'Request timed out', 'query': query}
    except requests.RequestException:
        error = repr(format_exc)
        google_result = {'result': None, 'message': error, 'query': query}
    return google_result

@shared_task
def duck_duck_go(query):
    import requests
    duck_duck_go_api = "http://api.duckduckgo.com/?q={query}&format=json".format(query=query)
    try:
        duck_duck_go_result = requests.get(duck_duck_go_api, timeout=1).json()
        duck_duck_go_result = {'result': duck_duck_go_result, 'query': query}
    except requests.exceptions.Timeout:
        duck_duck_go_result = {'result': None, 'message': 'Request timed out', 'query': query}
    except requests.RequestException:
        error = repr(format_exc)
        duck_duck_go_result = {'result': None, 'message': error, 'query': query}

    return duck_duck_go_result

@shared_task
def twitter(query):
    import tweepy
    API_KEY = "CEiNihr0GDvuvo4zsa9eEkcAB"
    API_SECRET = "zi3uyW6dqanVvotwdz3sG3ST1rLRCvgF2FVpNvgjMiaZoALo1z"
    auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
    api = tweepy.API(auth, timeout=1)

    try:
        twitter_result = api.search(q=query, count=10, result_type='recent')
        twitter_result = [{'text': t.text} for t in twitter_result]
        twitter_result = {'result': twitter_result, 'query': query}
    except tweepy.error.TweepError:  # No special exception for TimeOut
        twitter_result = {'result': None, 'message': 'Request timed out', 'query': query}

    return twitter_result
