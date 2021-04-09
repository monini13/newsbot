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
    URL = "https://www.economist.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')
    url_dic = dict()
    title_dic = dict()
    idx = 0
    for _,a in enumerate(soup.find_all('a',{"class":"headline-link"}, href=True)):
        if validators.url(URL + a['href']):
            url_dic[idx] = URL + a['href']
            title_dic[idx] = a.text
            idx += 1
    return url_dic, title_dic

def get_economist_news(page):
    """
    Args
        page (requests.get): url page to specific economist news webpage
    Returns:
        out (list): list of article paragraph text compiled from economist webpage
    """
    soup = BeautifulSoup(page.content,'html.parser')
    paragraphs = soup.find_all("p",{"class":"article__body-text"})
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

