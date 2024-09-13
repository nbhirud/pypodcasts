# from xml.etree import ElementTree
# from urllib import request
# from xml.dom import minidom
from io import text_encoding
from re import L
import requests
from pathlib import Path
import speech_recognition as sr
from torch import segment_reduce
import whisper
import chime
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Sequence, Tuple, Union
from whisper import DecodingResult

# Wordcloud stuff:
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from pypodcasts.prepare import clean

# LLM
import ollama



# pip install chime
# >>> chime.success()
# >>> chime.warning()
# >>> chime.error()
# >>> chime.info()
# >>> chime.themes()
# ['big-sur', 'chime', 'mario', 'material', 'pokemon', 'sonic', 'zelda']
# >>> chime.theme('zelda')

# CONSTANTS
BASE_DIR = Path(__file__).parent
AUDIO_PATH = "pypodcasts/media/audio"
TRANSCRIPT_PATH = "pypodcasts/media/transcript"
WORDCOUNT_PATH = "pypodcasts/media/wordcount"

def whisper_transcribe(audio_filepath:str, model_name:str="base.en"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_filepath)
    # print(result["text"])
    # text = result["text"]
    # segment = result["text"]
    # language = result["text"]
    return result["text"]
    
    
def whisper_decode(audio_filepath:str, model_name:str="base") -> Union[DecodingResult, List[DecodingResult]]:
    # TODO - Returns only a small part. Probably I am returning only a small part and need to refine this
    
    model = whisper.load_model(model_name)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_filepath)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    # print(result.text)
    # if isinstance(result, list):
    #     result = result[0]
    # language
    # text

    return result


def create_wordcoud(transcript_filepath:str):
    # can pass text directly, but this approach of communicating through files is to ensure decoupling
    with open(transcript_filepath, mode="r") as file:
        text = file.read()
    clean_text = clean(text)
    wc = WordCloud(max_words=30,width = 800, height = 500).generate(clean_text)
    # plt.axis("off")
    # plt.imshow(wc)
    return wc
    
# The user would input a URL when they wish to play/read episodes from a new RSS feed. 
# get user input. Let's say user inputs "https://talkpython.fm/subscribe/rss"
# It is possible that the URL entered is of a podcast that has already been fetched. 
# The above podcast has the following different URL in the XML:
# <atom:link href="https://talkpython.fm/episodes/rss" rel="self" type="application/rss+xml"/>
# The XML actually does not contain https://talkpython.fm/subscribe/rss anywhere in it. 
# The developer in me tells me that I should care about only the URL in the XML (https://talkpython.fm/episodes/rss)
# But the better developer in me tells me that I should not keep downloading the same XML again and again every time because 
# the URL I stored doesn't match the one the user entered even though they belong to the same podcast.
# Also, to know the title from the URL, you first need to doenload the XML.
# Right now, I think I will store the entered URL/s and the URL from XML against the title.


# RSS title : url
rss_remembered = {
    "Talk Python To Me": "https://talkpython.fm/subscribe/rss"
}







podcast_channel_url = rss_remembered.get("Talk Python To Me")
# query_parameters = {"downloadformat": "json"}


if not Path(transcript_filepath).exists():
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

audio_filename = audio_file_url.split("/")[-1]
audio_filepath = f"{AUDIO_PATH}/{audio_filename}"

filename_base = audio_filename.split(".")[0]

transcript_filename = f"{filename_base}.txt"
transcript_filepath = f"{TRANSCRIPT_PATH}/{transcript_filename}"

wordcount_filename = f"{filename_base}.png"
wordcount_filepath = f"{WORDCOUNT_PATH}/{wordcount_filename}"

# Save the audio file to file:
if not Path(audio_filepath).exists():
    response = requests.get(audio_file_url)
    with open(audio_filepath, mode="wb") as file:
        file.write(response.content)

# Speech to Text - create transcript file
if not Path(transcript_filepath).exists():
    text=""
    if audio_filename.endswith(".wav"):
        r = sr.Recognizer() # Does not support mp3 files
        afile = sr.AudioFile(audio_filepath)
        with afile as source:
            audio = r.record(source)
            r.recognize_google(audio)
    # elif audio_filename.endswith(".mp3"):
    #     # espnet
    #     pass
    else:
        # openai-whisper # requires ffmpeg # https://github.com/openai/whisper # may need setuptools-rust # works better on computers with a GPU
        # text = whisper_decode(audio_filepath=audio_filepath)
        text = whisper_transcribe(audio_filepath=audio_filepath)
        pass

    with open(transcript_filepath, mode="w") as file:
        file.write(str(text))
        # print(text)

# Create wordcount image using transcript
if not Path(wordcount_filepath).exists():
    wc = create_wordcoud(transcript_filepath=transcript_filepath)
    wc.to_file(filename=wordcount_filepath)
wc = plt.imread(wordcount_filepath)
plt.axis("off")
plt.imshow(wc)





# Some LLM stuff
response = ollama.chat(model='llama3.1', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])


chime.success()
print("done")


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







