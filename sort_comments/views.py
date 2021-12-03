from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


# Create your views here.
def index(request):
    base_url = "https://habr.com/ru/post/591109/comments/"
    r = requests.get(base_url)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    # comments = soup.find("div", {"class": "tm-comments__tree"})
    comments = soup.find_all("article", {"class": "tm-comment-thread__comment"})
    all_comments = []
    i = 0
    for article in comments:
        comment = {}
        # try/except для отлова удаленных комментариев
        try:
            comment['username'] = article.find("a", {"class": "tm-user-info__userpic"}).get('title')
            comment['user_url'] = "https://habr.com" + article.find("a", {"class": "tm-user-info__username"})['href']
            comment['time'] = article.find("a", {"class": "tm-comment-thread__comment-link"}).get_text().strip()
            # comment['raw_comment'] = str(article.find("div", {"class": "tm-comment__body-content"}).contents[0])
            comment['raw_comment'] = str(article.find("div", {"class": "tm-comment__body-content"}))
            comment['comment_url'] = base_url + article.find("a", {"class": "tm-comment-thread__comment-link"}).get(
                'href')
            comment['score'] = article.find("span", {"class": "tm-votes-meter__value_rating"}).get_text()
            comment['score'] = int(comment['score'].replace("+", "").replace("–", "-"))
            comment['id'] = i
            i += 1
            all_comments.append(comment)
        except:
            pass

    all_comments.sort(key=lambda d: d['score'], reverse=True)

    return render(request, "index.html", {'comments': all_comments})
