import requests
from bs4 import BeautifulSoup


def get_posts():
    # Access blog and get HTML
    response = requests.get('https://nymarya.github.io/categories')
    html_data = response.text

    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html_data, features="html.parser")

    posts = {}

    # Find categories
    categories = soup.findAll("h2")

    # For each language/category, extract title and link of newest post
    for category in categories:
        lang = category.next_element  # eng/pt-br
        recent_post = category.findNext('a')
        posts[lang] = {'link': recent_post['href'],
                       'title': recent_post['title']}

    return posts
