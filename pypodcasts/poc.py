# from xml.etree import ElementTree
# from urllib import request
# from xml.dom import minidom
import requests
import speech_recognition as sr

# CONSTANTS
AUDIO_PATH = "pypodcasts/media/audio"

podcast_channel_url = "https://talkpython.fm/subscribe/rss"
# query_parameters = {"downloadformat": "json"}

# response = requests.get(podcast_channel_url, params=query_parameters)
response = requests.get(podcast_channel_url)


# print(response.url)
# print(response.ok)
# print(response.status_code)



# with open("rss_tptm.rss", mode="wb") as file:
#     file.write(response.content)


content = response.content

# print(content)


# with open("pypodcasts/rss_tptm.rss", mode="r") as file:
#     rssfile = file.read()
#     print(rssfile)



audio_file_url = "https://talkpython.fm/episodes/download/475/python-language-summit-2024.mp3"
response = requests.get(audio_file_url)
audio_filename = audio_file_url.split("/")[-1]
audio_file_path = f"{AUDIO_PATH}/{audio_filename}"

# with open(audio_file_path, mode="wb") as file:
#     file.write(response.content)

# Speech to Text:

if audio_filename.endswith(".wav"):
    r = sr.Recognizer() # Does not support mp3 files
    afile = sr.AudioFile(audio_file_path)
    with afile as source:
        audio = r.record(source)
        r.recognize_google(audio)
elif audio_filename.endswith(".mp3"):
    #TODO
    pass
# pip wheel --no-cache-dir --use-pep517 "numpy (==1.23.5)"
# poetry add numpy
# poetry add openai-whisper llvmlite


# dom = ""
# title = ""
# link = ""
# published = ""
#
# # download the xml document
# with request.urlopen(podcast_channel_url) as res:
#     dom = minidom.parseString(res.read().decode('latin-1'))
#     title = dom.getElementsByTagName('title')[0].firstChild.nodeValue
#     link = dom.getElementsByTagName('link')[0].getAttribute('href')
#     #published = dom.getElementsByTagName('published')[0].firstChild.nodeValue
#
#
# print("dom = ", dom)
# print("title = "" = ", title)
# print("link = ", link)
# print("published = ", published)
#
# # # Parse the XML document
# tree = ElementTree.parse(dom)
#
# # # Proof of concept
# print()
#
# # print(tree)







