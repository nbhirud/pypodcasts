# from xml.etree import ElementTree
# from urllib import request
# from xml.dom import minidom
import requests

podcast_channel_url = "https://talkpython.fm/subscribe/rss"
# query_parameters = {"downloadformat": "json"}

# response = requests.get(podcast_channel_url, params=query_parameters)
response = requests.get(podcast_channel_url)


print(response.url)
print(response.ok)
print(response.status_code)



# with open("rss_tptm.rss", mode="wb") as file:
#     file.write(response.content)


content = response.content

print(content)






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







