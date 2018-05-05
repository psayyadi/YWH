
"""
Created on Fri Apr 13 21:50:41 2018
Python Version 3.6.4
This code contains functions to read the downloaded watch history from google
account.

@author: Peyman Sayyadi
"""
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import codecs
import re
import csv
import requests
from collections import Counter
import pygal

#The youtube codes that identify the categories of videos
DEF_DICT = {'2': 'Autos & Vehicles', '1': ' Film & Animation',
           '10': 'Music', '15': 'Pets & Animals', '17': 'Sports',
           '18': 'Short Movies', '19': 'Travel & Events', '20': 'Gaming',
           '21': 'Videoblogging', '22': 'People & Blogs', '23': 'Comedy',
           '24': 'Entertainment', '25': 'News & Politics', '26': 'How to & Style',
           '27': 'Education', '28': 'Science & Technology',
           '29': 'Nonprofits & Activism', '30': 'Movies', '31': 'Anime/Animation',
           '32': 'Action/Adventure', '33': 'Classics', '34': 'Comedy',
           '35': 'Documentary', '36': 'Drama', '37': 'Family', '38': 'Foreign',
           '39': 'Horror', '40': 'Sci-Fi/Fantasy', '41': 'Thriller',
           '42': 'Shorts', '43': 'Shows', '44': 'Trailers'}

#The path of the downloaded file on the local disc
my_url = '/Users/MEHRA/Documents/Notebooks/Takeout 3/YouTube/history/watch-history.html'
#Developer key which should be obtained from your developer account
DEVELOPER_KEY = 'your key'

def video_data(v_id):
    """
    Reads the youtube page snippet and refines it with
    selected info into a dictionary that contains the video title, channel title,
    publish date, category id and the video's unique url code.
    The api key needs to be obtained and inserted in the DEVELOPER_KEY constant.
    """
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}"
    r = requests.get(url.format(id=v_id, api_key=DEVELOPER_KEY))
    js = r.json()
    items = js["items"][0]
    video_dic = {}
    video_dic['title'] = items["snippet"]['title']
    video_dic['channelTitle'] = items["snippet"]['channelTitle']
    video_dic['publishedAt'] = items["snippet"]['publishedAt']
    video_dic['categoryId'] = items["snippet"]['categoryId']
    video_dic['urlcode']=v_id
    return video_dic

# Parsing the html file
def dates_and_codes(url):
    """
    reads the downloaded watch history and extracts the information into a
    dictionnary.
    input:
        url: the local path to the html file downloaded from google account.
    output:
        watch_dic_list: a list of dictionnaries containing the information of all the videos
        in the watch history.
    """
    f=codecs.open(url, 'r')
    soup = BeautifulSoup(f, 'html.parser')
    # pattern for for recognizing the date
    pattern = re.compile(r'[A-Z][a-z][a-z]\s\d{1,2},\s20\d\d,\s.{9,10}M')
    dates = pattern.findall(str(soup))
    terms = soup.find_all('a')
    j = 0
    watch_dic_list = []
    for term in terms:
        if 'watch' in term.get('href'):
            vid_id = term.get('href')[32:]
            try:
                watch_dic = video_data(vid_id)
                watch_dic['watch_date'] = dates[j]
            except:
                #Not all the information can be extracted from youtube, I guess
                #this is because those videos are no longer available. Any infro or
                #help on this would be appreciated.
                watch_dic = 'Exception happened'
            watch_dic_list.append(watch_dic)
            j += 1
    return watch_dic_list
# print(dates_and_codes(my_url))

# plot_histogram(my_file)
def plot_piechart(watch_dic):
    """
    Plotting the number of views based on categoryId defined by youtubeself.
     """
    vcat = []
    for video in watch_dic:
        try:
            vcat.append(video['categoryId'])
        except:
            continue
    letter_counts = Counter(vcat)
    new_letter_counts = {}
    for num, count in letter_counts.items():
        try:
            key = DEF_DICT[num]
            new_letter_counts[key] = count
        except:
            continue
    sorted_letter_counts = sorted(new_letter_counts.items(), key = lambda t:t[1],reverse = True)
    pie_chart = pygal.Pie(print_values=True, width =1200)
    # pie_chart.title = 'youtube watches categories'
    for cat in sorted_letter_counts:
        pie_chart.add(cat[0], cat[1])
    pie_chart.render_in_browser()

plot_piechart(dates_and_codes(my_url))
