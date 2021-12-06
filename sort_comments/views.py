from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re


# Create your views here.
def index(request):
    if request.method == 'POST':
        base_url = request.POST['habr_url']
        if not base_url.endswith('comments/', -9):
            if base_url.endswith('/', -1):
                base_url = base_url + 'comments/'
            else:
                base_url = base_url + '/comments/'
    else:
        base_url = "https://habr.com/ru/post/592135/"
        return render(request, "index.html", {'habr_url': base_url})

    r = requests.get(base_url)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    comments = soup.find_all("article", {"class": "tm-comment-thread__comment"})
    all_comments = []
    for article in comments:
        comment = {}
        # try/except для отлова удаленных комментариев
        try:
            comment['username'] = article.find("a", {"class": "tm-user-info__userpic"}).get('title')
            comment['user_url'] = "https://habr.com" + article.find("a", {"class": "tm-user-info__username"})['href']
            comment['time'] = article.find("a", {"class": "tm-comment-thread__comment-link"}).get_text().strip()
            comment['raw_comment'] = str(article.find("div",
                                                      {"class": "tm-comment__body-content"})).replace("<br/>", "")
            comment['comment_url'] = base_url + article.find("a",
                                                             {"class": "tm-comment-thread__comment-link"}).get('href')
            comment['score'] = article.find("span", {"class": "tm-votes-meter__value_rating"}).get_text()
            comment['score'] = int(comment['score'].replace("+", "").replace("–", "-"))
            votes = re.findall(r'↑\d+|↓\d+',
                               article.find("span", {"class": "tm-votes-meter__value_rating"}).get('title'))
            comment['controversy'] = min(int(votes[0][1:]), int(votes[1][1:]))
            comment['votes'] = votes[0] + ' ' + votes[1]
            all_comments.append(comment)
        except:
            pass

    if request.POST.get('Sort By:') == 'top':
        all_comments.sort(key=lambda d: d['score'], reverse=True)
    elif request.POST.get('Sort By:') == 'controversial':
        all_comments.sort(key=lambda d: d['controversy'], reverse=True)

    return render(request, "index.html", {'comments': all_comments, 'habr_url': base_url[:-9]})
