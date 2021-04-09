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
    URL = "https://www.reuters.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')
    url_dic = dict()
    title_dic = dict()
    idx = 0
    for a in soup.find_all("div",{"class":"story-content"}):
        temp = a.find_all("h3",text=True)
        if temp:
            if validators.url(URL + a.find_all("a",href=True)[0]['href']):
                url_dic[idx] = URL + a.find_all("a",href=True)[0]['href']
                title_dic[idx] = temp[0].text.strip()
                idx += 1
    # print(url_dic)
    return url_dic, title_dic

def get_reuters_news(page):
    """
    Args
        page (requests.get): url page to specific economist news webpage
    Returns:
        out (list): list of article paragraph text compiled from economist webpage
    """
    soup = BeautifulSoup(page.content,'html.parser')
    paragraphs = soup.find_all("p",{'class':"Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x"})
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

