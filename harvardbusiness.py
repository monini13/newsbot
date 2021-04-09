import requests
from bs4 import BeautifulSoup
import validators

def get_headlines():
    """
    Args:
        None
    Returns:
        url_dic    (dict): dictionary consisting of index to url of economist news
        title_dic  (dict): dictionary consiste of index to title of economist news
    """
    URL = "https://hbr.org/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')
    url_dic = dict()
    title_dic = dict()
    out = soup.find_all('h3',{"class":"hed"})
    idx = 0
    for _, news in enumerate(out):
        title = news.find_all(text=True)[0]
        link = news.find_all(href=True)[0]['href']
        if validators.url(URL + link):
            url_dic[idx] = URL + link
            title_dic[idx] = title
            idx+=1
    return url_dic, title_dic

def get_hbr_news(page):
    """
    Args
        page (requests.get): url page to specific economist news webpage
    Returns:
        out (list): list of article paragraph text compiled from economist webpage
    """
    soup = BeautifulSoup(page.content,'html.parser')
    paragraphs = soup.find_all("p")
    # print(len(paragraphs))
    out = [""]
    total = 0
    MAX = 4096
    for paragraph in paragraphs:
        paragraph = paragraph.text + "\n\n"
        if total + len(paragraph) > MAX:
            out.append(paragraph)
            total = len(paragraph)
        else:
            out[-1] += paragraph
            total += len(paragraph)

    return out

